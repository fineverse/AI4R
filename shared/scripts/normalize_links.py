#!/usr/bin/env python3
"""把工作空间内所有 Markdown 相对链接规范化为「相对当前文件位置」的标准形式，并报告死链。

幂等：对已规范的链接再跑一次结果不变。不含任何删除动作。
用法：python3 normalize_links.py [--apply]
"""
import os
import re
import sys

ROOT = '/home/verse/dev/AI4R'
REPOS = os.path.join(ROOT, 'projects/autonomous-driving/topics/diffusion-planner/code/repos')
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
APPLY = '--apply' in sys.argv

count = 0
bad = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    if REPOS in dirpath or '/.git' in dirpath or '/.trae' in dirpath:
        continue
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

        new_text = LINK_RE.sub(repl, text)
        if APPLY and new_text != text:
            open(path, 'w', encoding='utf-8').write(new_text)

print('检查链接 %d 处；死链 %d 处' % (count, len(bad)))
for src, link in bad:
    print('   %s  ->  %s' % (src, link))
