#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse CCF 2026 PDF (bbox HTML export) into structured records.

Pipeline:
  bbox HTML -> word-level lines -> column classification per table entry
  -> recover dropped trailing continuation lines (page-end artifacts)
  -> extract （原 ...） aliases -> (optional) verified overrides for scrambled rows
"""
import re, html, json, sys, collections

import os as _os
# 中间产物根：工作空间**内**（第四十八轮起；/tmp 在权限自动允许范围之外，每次访问都会弹授权）
# 见 ai/rules.md §执行与清理纪律第 1 条。可用环境变量覆盖。
_SCRATCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'inbox', 'scratch'))
SRC = _os.environ.get('CCF_BBOX_HTML', _os.path.join(_SCRATCH, 'ccf2026_bbox.html'))
RAW = _os.environ.get('CCF_RAW_TXT', _os.path.join(_SCRATCH, 'ccf2026_raw.txt'))
OUT = _os.environ.get('CCF_OUT_JSON', _os.path.join(_SCRATCH, 'ccf2026_parsed.json'))

AREAS = [
 '计算机体系结构/并行与分布计算/存储系统',
 '计算机网络',
 '网络与信息安全',
 '软件工程/系统软件/程序设计语言',
 '数据库/数据挖掘/内容检索',
 '计算机科学理论',
 '计算机图形学与多媒体',
 '人工智能',
 '人机交互与普适计算',
 '交叉/综合/新兴',
]
AREA_ORDER = {a: i for i, a in enumerate(AREAS)}
CLASS_ORDER = {'A': 0, 'B': 1, 'C': 2}

URL_SIG = re.compile(r'https?://|www\.|dblp|trier\.de|\.html|scitation|pubs\.asha|journals\.elsevier|\.org/|\.com/|\.de/|doi\.org')
CJK = re.compile(r'[\u4e00-\u9fff]')
ALIAS_RE = re.compile(r'[（(]\s*原\s*([^）)]+)[）)]')

def is_cjk(ch):
    return bool(CJK.match(ch))

def join_words(words):
    out = ''
    for w in words:
        t = w['text'] if isinstance(w, dict) else w
        if out:
            pc, nc = out[-1], t[0]
            if not (is_cjk(pc) and is_cjk(nc)):
                out += ' '
        out += t
    return out

def join_url(words):
    return ''.join(w['text'] for w in words)

def clean_parens(s):
    s = re.sub(r'\s+（', '（', s)
    s = re.sub(r'）\s+', '）', s)
    s = re.sub(r'-\s+', '-', s)
    s = re.sub(r'\s+-', '-', s)
    s = re.sub(r'\+\s+', '+', s)
    s = re.sub(r'\s+\+', '+', s)
    s = re.sub(r'/\s+', '/', s)
    s = re.sub(r'\s+/', '/', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_pages(src):
    pat_word = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
    pat_page = re.compile(r'<page[^>]*>(.*?)</page>', re.S)
    pages = []
    for m in pat_page.finditer(src):
        words = []
        for w in pat_word.finditer(m.group(1)):
            xmin, ymin, xmax, ymax = map(float, w.groups()[:4])
            text = html.unescape(w.group(5))
            words.append(dict(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, text=text))
        words.sort(key=lambda t: (t['ymin'], t['xmin']))
        lines = []
        cur = []
        last = None
        for w in words:
            if last is None or abs(w['ymin'] - last) <= 5.0:
                cur.append(w)
            else:
                lines.append(cur); cur = [w]
            last = w['ymin']
        if cur:
            lines.append(cur)
        pages.append(lines)
    return pages

def line_text(line):
    return ' '.join(w['text'] for w in line)

def classify_line(line):
    t = line_text(line)
    if '和期刊目录' in t:
        return 'cover', None
    if '中国计算机学会推荐国际学术期刊' in t and '会议' not in t:
        return 'title', 'journal'
    if '中国计算机学会推荐国际学术会议' in t:
        return 'title', 'conference'
    m = re.search(r'[（(]([^（）()]+)[）)]', t)
    if m and m.group(1) in AREAS:
        return 'area', m.group(1)
    if re.match(r'^[一二三]、\s*[ABC]\s*类', t):
        cm = re.search(r'[ABC]', t)
        return 'class', cm.group(0)
    if '序号' in t and '简称' in t and ('全称' in t or '网址' in t):
        return 'table_header', None
    if max(w['xmax'] for w in line) < 30:
        return 'junk', None
    if min(w['ymin'] for w in line) < 40:
        return 'junk', None
    return 'content', None

def cluster_words(words):
    ws = sorted(words, key=lambda w: w['xmin'])
    clusters = []
    cur = [ws[0]]
    for w in ws[1:]:
        if w['xmin'] - cur[-1]['xmax'] <= 10.0:
            cur.append(w)
        else:
            clusters.append(cur); cur = [w]
    clusters.append(cur)
    return clusters

def find_number(line):
    for w in line['words']:
        if re.fullmatch(r'\d+', w['text']) and w['xmin'] < 120:
            return int(w['text'])
    return None

def extract_aliases(rec):
    """Pull （原 ...）/（原...） notes out of abbreviation/full_name/publisher."""
    aliases = []
    former_publishers = []
    for field in ('abbreviation', 'full_name'):
        v = rec.get(field, '')
        def repl(m):
            aliases.append(m.group(1).strip())
            return ''
        rec[field] = re.sub(r'\s+', ' ', ALIAS_RE.sub(repl, v)).strip()
    v = rec.get('publisher', '')
    def repl_pub(m):
        former_publishers.append(m.group(1).strip())
        return ''
    rec['publisher'] = re.sub(r'\s+', ' ', ALIAS_RE.sub(repl_pub, v)).strip()
    rec['aliases'] = aliases
    rec['former_publishers'] = former_publishers
    return rec

# Verified overrides for rows where the PDF's text boxes overlap so badly that
# positional extraction scrambles the words. Values taken from pdftotext raw output.
OVERRIDES = {
    # (area, kind, rank, number)
    ('计算机图形学与多媒体', 'conference', 'C', 2): dict(  # CASAXR
        abbreviation='CASAXR',
        full_name='International Conference on Computer Animation, Social Agents, and Extended Reality',
        publisher='Wiley',
        url='http://dblp.uni-trier.de/db/conf/ca/',
        aliases=['CASA', 'International Conference on Computer Animation and Social Agents'],
        former_publishers=[]),
    ('交叉/综合/新兴', 'journal', 'C', 12): dict(  # EITEE
        abbreviation='EITEE',
        full_name='ENGINEERING Information Technology & Electronic Engineering',
        publisher='浙江大学出版社',
        url='https://www.academax.com/EITEE/home',
        aliases=['FITEE', 'Frontiers of Information Technology & Electronic Engineering'],
        former_publishers=['Springer']),
    ('计算机图形学与多媒体', 'journal', 'B', 9): dict(  # CVMJ
        abbreviation='CVMJ',
        full_name='Computational Visual Media',
        publisher='清华大学出版社/IEEE',
        url='https://dblp.org/db/journals/cvm/index.html',
        aliases=[],
        former_publishers=['Tsinghua University/Springer']),
}

def main():
    src = open(SRC, encoding='utf-8').read()
    pages = parse_pages(src)

    # Pass 1: classify lines, maintain state, collect content lines + anchors
    content = []
    kind = area = cls = None
    table_id = 0
    table_active = False
    for pno, lines in enumerate(pages):
        for line in lines:
            typ, val = classify_line(line)
            if typ == 'cover':
                kind = area = cls = None; table_active = False
            elif typ == 'title':
                kind = val; area = None; cls = None; table_active = False
            elif typ == 'area':
                area = val
            elif typ == 'class':
                cls = val
            elif typ == 'table_header':
                table_id += 1
                table_active = True
            elif typ == 'content' and table_active and kind and area and cls:
                y = sum(w['ymin'] for w in line) / len(line)
                content.append(dict(page=pno, y=y, words=line, kind=kind, area=area, cls=cls, table_id=table_id))

    anchor_idx = [i for i, l in enumerate(content) if find_number(l) is not None]
    if not anchor_idx:
        print('NO ANCHORS FOUND', file=sys.stderr); sys.exit(1)

    # Pass 2: segment content into entries using largest-gap boundaries
    entries = []
    n = len(content)
    claimed = [False] * n

    def gap_between(i, j):
        a, b = content[i], content[j]
        if a['page'] != b['page']:
            return 1e9
        return b['y'] - a['y']

    for k, ai in enumerate(anchor_idx):
        num = find_number(content[ai])
        if k == 0:
            start = 0
        else:
            prev_ai = anchor_idx[k - 1]
            best_b, best_g = prev_ai, -1
            for b in range(prev_ai, ai):
                g = gap_between(b, b + 1)
                if g > best_g:
                    best_g, best_b = g, b
            start = best_b + 1
        lines = content[start:ai + 1]
        for idx in range(start, ai + 1):
            claimed[idx] = True
        entries.append(dict(number=num, lines=lines, kind=content[ai]['kind'],
                            area=content[ai]['area'], cls=content[ai]['cls'],
                            table_id=content[ai]['table_id']))
    last_ai = anchor_idx[-1]
    if last_ai + 1 < n:
        entries[-1]['lines'].extend(content[last_ai + 1:])
        for idx in range(last_ai + 1, n):
            claimed[idx] = True

    # Recover dropped lines: trailing continuation lines at page ends that the
    # largest-gap boundary (cross-page gap = 1e9) left unclaimed. Each such line
    # belongs to the entry whose last claimed line is immediately before it on the
    # same page.
    dropped = [i for i, c in enumerate(claimed) if not c]
    for i in dropped:
        target = None
        for e in entries:
            el = e['lines'][-1]
            if el['page'] == content[i]['page'] and content[i]['y'] > el['y']:
                if target is None or (el['page'], el['y']) > (target['lines'][-1]['page'], target['lines'][-1]['y']):
                    target = e
        if target is not None:
            target['lines'].append(content[i])
            claimed[i] = True
    if any(not c for c in claimed):
        print(f'WARNING: {sum(1 for c in claimed if not c)} lines still unclaimed', file=sys.stderr)

    # Pass 3: per-entry url_left = leftmost URL_SIG cluster of that entry
    # (per-table min is unreliable: in some tables the URL column starts further
    #  left than other rows' publisher column, swallowing publishers as URLs)
    url_left = {}
    for e in entries:
        lefts = []
        for ln in e['lines']:
            for w in ln['words']:
                if URL_SIG.search(w['text']):
                    lefts.append(w['xmin'])
        url_left[id(e)] = (min(lefts) - 1.5) if lefts else float('inf')

    # Pass 4: classify cells per entry
    records = []
    problems = []
    for e in entries:
        clusters = []
        for ln in e['lines']:
            for cl in cluster_words(ln['words']):
                clusters.append(dict(words=cl, xmin=cl[0]['xmin'], xmax=cl[-1]['xmax'],
                                     y=ln['y'], page=ln['page']))
        clusters.sort(key=lambda c: (c['page'], c['y'], c['xmin']))
        ul = url_left[id(e)]
        number = None
        url_w = []; abbr_w = []; full_w = []; pub_w = []
        for c in clusters:
            txt = ''.join(w['text'] for w in c['words'])
            if re.fullmatch(r'\d+', txt) and c['xmin'] < 120:
                number = int(txt)
                continue
            if URL_SIG.search(txt) or c['xmin'] >= ul:
                url_w.extend(c['words'])
                continue
            if c['xmax'] <= 235:
                abbr_w.extend(c['words'])
                continue
            if c['xmin'] >= 400:
                pub_w.extend(c['words'])
                continue
            full_w.extend(c['words'])
        wpos = {}
        for ln in e['lines']:
            for w in ln['words']:
                wpos[id(w)] = (ln['page'], ln['y'])
        def wkey(w):
            p, y = wpos[id(w)]
            return (p, y, w['xmin'])
        abbr_w.sort(key=wkey); full_w.sort(key=wkey); pub_w.sort(key=wkey); url_w.sort(key=wkey)

        abbr = clean_parens(join_words(abbr_w))
        full = clean_parens(join_words(full_w))
        pub = clean_parens(join_words(pub_w))
        url = re.sub(r'(https?://)', r' \1', join_url(url_w)).strip()
        if number is None:
            problems.append(('no-number', full, abbr))
        if not full_w:
            problems.append(('no-fullname', abbr, url))
        if not url_w:
            problems.append(('no-url', abbr, full))
        pages = sorted(set(ln['page'] for ln in e['lines']))
        records.append(dict(
            area=e['area'], kind=e['kind'], rank=e['cls'], number=number,
            abbreviation=abbr, full_name=full, publisher=pub, url=url,
            source_pages=[p + 1 for p in pages],
        ))

    # Pass 5: alias extraction + verified overrides
    for r in records:
        key = (r['area'], r['kind'], r['rank'], r['number'])
        if key in OVERRIDES:
            r.update(OVERRIDES[key])
        else:
            extract_aliases(r)

    # sort records: area order, kind (journal first), class, number
    records.sort(key=lambda r: (AREA_ORDER[r['area']], 0 if r['kind'] == 'journal' else 1,
                                CLASS_ORDER[r['rank']], r['number'] or 0))
    return records, problems

if __name__ == '__main__':
    if len(_os.sys.argv) > 1:
        SRC = _os.sys.argv[1]
    if len(_os.sys.argv) > 2:
        OUT = _os.sys.argv[2]
    records, problems = main()
    print(f"TOTAL RECORDS: {len(records)}")
    from collections import Counter
    c = Counter((r['area'], r['kind'], r['rank']) for r in records)
    for k in sorted(c, key=lambda x: (AREA_ORDER[x[0]], 0 if x[1]=='journal' else 1, CLASS_ORDER[x[2]])):
        print(f"  {k[0][:12]:<14} {k[1]:<10} {k[2]}: {c[k]}")
    print("PROBLEMS:", len(problems))
    for p in problems[:40]:
        print("  ", p)
    json.dump(records, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
