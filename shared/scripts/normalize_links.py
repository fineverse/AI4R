#!/usr/bin/env python3
"""把工作空间内所有 Markdown 相对链接规范化为「相对当前文件位置」的标准形式，并报告死链。

幂等：对已规范的链接再跑一次结果不变。不含任何删除动作。
用法：python3 normalize_links.py [--apply]
"""
import os
import re
import sys

ROOT = '/home/verse/dev/AI4R'
# 跳过目录（与 check_links.py 的 SKIP_DIRS 同口径，按目录名剪枝）：
# · repos = 第三方代码快照（1.65 GB），实际位置在项目根 code/repos——第七十七轮修正：此前排除
#   路径写的是 2026-09-23 重构前的旧址 topics/diffusion-planner/code/repos，条件永不命中，
#   --apply 会误改快照内的链接；
# · archive = 归档件按约定「原样不回改」（其中链接记录的是历史位置，失效属预期）；
# · scratch = 临时产物根；.git / .trae / __pycache__ / node_modules = 非知识树。
SKIP_DIRS = {'.git', '.trae', 'repos', 'archive', 'scratch', '__pycache__', 'node_modules'}
LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)\s]+)\)')
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

        new_text = LINK_RE.sub(repl, text)
        if APPLY and new_text != text:
            open(path, 'w', encoding='utf-8').write(new_text)

print('检查链接 %d 处；死链 %d 处' % (count, len(bad)))
for src, link in bad:
    print('   %s  ->  %s' % (src, link))
