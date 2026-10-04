#!/usr/bin/env python3
"""把工作空间内所有 Markdown 相对链接规范化为「相对当前文件位置」的标准形式，并报告死链。

幂等：对已规范的链接再跑一次结果不变。不含任何删除动作。
用法：python3 normalize_links.py [--apply]
"""
import os
import re
import sys

# 工作空间根 = 本脚本上溯两级（shared/scripts/ → 工作空间根）；用 __file__ 派生，迁移换路径不用改
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 跳过目录（与 check_links.py 的 SKIP_DIRS 同口径，按目录名剪枝）：
# · repos = 第三方代码快照（1.65 GB），实际位置在项目根 code/repos——第七十七轮修正：此前排除
#   路径写的是 2026-09-23 重构前的旧址 topics/diffusion-planner/code/repos，条件永不命中，
#   --apply 会误改快照内的链接；
# · archive = 归档件按约定「原样不回改」（其中链接记录的是历史位置，失效属预期）；
# · scratch = 临时产物根；.git / .trae / __pycache__ / node_modules = 非知识树。
SKIP_DIRS = {'.git', '.trae', '.vscode', 'repos', 'archive', 'scratch', '__pycache__', 'node_modules'}
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
# 行内代码跨度（`...` / ``...``）：里面的 `[x](y)` 是**举例**，不是真链接——与 check_links.py
# 同源的正则（第二十九轮在那里修过同类误报，第七十八轮回移到本脚本：此前对原始全文做 sub，
# 示例文本被当真链接重写，--apply 会改坏 rounds-45/29/33 等处的示例）。
code_span_re = re.compile(r"(`{1,2})(?!`)(?:(?!\1).)*?\1(?!`)")
APPLY = '--apply' in sys.argv

count = 0
bad = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for name in filenames:
        if not name.endswith('.md'):
            continue
        path = os.path.join(dirpath, name)
        try:
            text = open(path, encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue

        def repl(m):
            global count
            label, link = m.group(1), m.group(2)
            if link.startswith(('http://', 'https://', 'mailto:', 'file:', '#')):
                return m.group(0)
            rel, sep, anchor = link.partition('#')
            if not rel:
                return m.group(0)
            target = os.path.normpath(os.path.join(dirpath, rel))
            new_rel = os.path.relpath(target, dirpath)
            if anchor:
                new_rel = new_rel + '#' + anchor
            count += 1
            if not os.path.exists(target):
                bad.append((os.path.relpath(path, ROOT), link))
            return '[%s](%s)' % (label, new_rel)

        # 逐行处理：``` 围栏内的行原样保留（模板示例不是真链接）；
        # 围栏外的行先把行内代码跨度**遮蔽为哨兵**（不是删除）再做链接替换、最后还原——
        # 与 check_links.py 同款豁免（第二十九轮修过同类误报）。
        # ⚠ 修复（第七十九轮）：此前写成 code_span_re.sub('', line)，会把行内代码整段删掉后写回
        #   （--apply 会破坏全库反引号内容）；改为哨兵遮蔽，行内代码原样保留。
        def protect(line):
            spans = []

            def stash(m):
                spans.append(m.group(0))
                return '\x00%d\x00' % (len(spans) - 1)

            masked = LINK_RE.sub(repl, code_span_re.sub(stash, line))
            for i, span in enumerate(spans):
                masked = masked.replace('\x00%d\x00' % i, span)
            return masked

        out_lines = []
        in_fence = False
        for line in text.split('\n'):
            if line.lstrip().startswith('```'):
                in_fence = not in_fence
                out_lines.append(line)
                continue
            if in_fence:
                out_lines.append(line)
                continue
            out_lines.append(protect(line))
        new_text = '\n'.join(out_lines)
        if APPLY and new_text != text:
            open(path, 'w', encoding='utf-8').write(new_text)

print('检查链接 %d 处；死链 %d 处' % (count, len(bad)))
for src, link in bad:
    print('   %s  ->  %s' % (src, link))
