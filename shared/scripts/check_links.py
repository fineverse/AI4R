#!/usr/bin/env python3
"""工作空间完整性检查（AI4R）。只读，不修改任何文件。

检查项（下面的列表**就是清单本身**）：
  1. 死链 —— 相对链接指向不存在的文件
  2. 行数预算 —— `index.md` / `state.md` 应 <=100 行
  3. 表格单元格数 —— 每行格数应等于表头列数（已处理 `\\|` 转义、跳过 ``` 围栏）
  4. 引用可达性 —— 孤儿文件 / 只被 `sources.md` 引用的"弱引用"
  5. 章节引用可达性 —— 链接文字里的 `§X` 必须**存在于链接目标那个文件里**：不在目标册但在它的
     册兄弟（`X-2.md`）里 → 报"错册"；两边都没有 → 报"目标文件里没有这一节"
  6. 笔记的「对本项目的意义」节 —— `notes/*.md` 必写（见 ai/templates.md）
  7. 小方向 README 的必写 4 节 —— `topics/<x>/README.md` 必写（见 ai/templates.md）
  8. 判断条数一致性 —— `judgments*.md` 的**实际 bullet 数**必须等于三处声明值
     （节标题的"（N 条）"、`judgments.md` 索引表的"条数"列、`state.md` 索引表的"条数"列与总条数）
  9. 声明计数 vs 权威源 —— 两个项目里那些"N 篇 / N 个 / N 条"的声明，必须等于从**文档之外的权威源**
     数出来的值（目录数 / 表格编号数 / 笔记文件数 / 章节行数）；规则登记在下方 `COUNT_RULES`
     （**措辞改了要更新登记表**，"声明处没匹配到"也会报出来）
  10. CSV 与 markdown 表的 ID 一致性 —— 每一对 `<x>.csv` + `<x>.md`（**双表示时 CSV 是权威源**），
      两边出现的 ID 集合必须**完全相同**（双向都报）；对子登记在下方 `CSV_ID_PAIRS`
  11. inbox 待整合 —— `inbox/` 根下的 `.md`（`cleanup.md` 除外）即"待整合投递物"，**非 0 即报**
      （2026-09-30 第六十二轮加；把"整合投递物"从人工 checklist 变成机器检查，见下）
  12. 文档体积预算 —— **任何文档 ≤ 64 KiB**（65536 字节，**Read 工具一次可整读的物理上限**）；
      **两线制**：硬线 64 KiB（超限即报、参与 exit code）、预警线 60 KiB（只报不阻断，留一轮增量余量）。
      阈值与「超限处理按文件角色分档」见 `ai/rules.md` §文件更新（2026-09-30 第六十四轮加；第七十四轮加预警线）
  13. README 轮次表完整性 —— README.md 链接到的单轮卷 `rounds-N.md`（纯数字；`rounds-24a.md` 与
      区间卷天然不匹配）必须 ① 覆盖到 `history/` 下实际最新一卷、② 在表内最小号与最大号之间无缺口
      （2026-10-01 第七十七轮加：第 67/68 轮收尾曾整行漏加，而漏行**不产生死链**——卷文件存在、
      history.md 也链接它，死链/孤儿检查都抓不到）
  14. `shared/index.md` 完整性 —— `shared/` **根**下每个 `.md`（`index.md` 自身除外）必须被
      `shared/index.md` 链接（2026-10-01 第七十九轮加：目录页漂移与 README 漏行同类，无警报）
  15. 投递物已入 git —— `inbox/` 待整合投递物（`cleanup.md` 除外）必须已被 git 跟踪
      （2026-10-01 第七十九轮加：未跟踪 = 覆盖后无法恢复，见 rules.md §支线协作纪律第 4 条）
  16. 轮次 tag —— `history/` 最新单轮卷 N 必须有 annotated tag `round-N`
      （2026-10-01 第七十九轮加：见 rules.md §执行与清理纪律第 9 条）

> **务实放弃项（第七十九轮）**：「中文命名锚点」检查（`§代码静态检查` 这类）经实现后**产生 37 处误报**——
> 中文章节锚与后文之间没有分隔符（`§轮次收尾第 7 步` / `§支线投递物 的结构写`），无法可靠切分，
> 故**不落盘**（按"永久报警必被无视"的教训）。替代：第 5 项的标题正则已收紧（`## 3 条…` 不再被当成 §3）。

**本清单不外传**（2026-09-30 第六十五轮收敛）：`shared/index.md` 与 `ai/workflows.md` 此前**各自又抄了一遍**这份清单，于是"十项 / 十一项 / 十二项"这个**数字在三处各写一次**——加一项就要改三处，**已实际漏过两次**（第 62、64 轮都是改了列表、忘了别处的总述）。现规定：**清单只在本 docstring 枚举；其余文档只写"见脚本 docstring"，不写数字、不列条目**。→ 这是「**引用可以重复，计数不能**」（[workflows.md](../../ai/workflows.md) §轮次收尾第 6 条）在**文档结构**上的应用。

跳过目录：`.git` / `repos`（第三方代码快照）/ `scratch`（临时产物根）/ `__pycache__` / `node_modules` / `archive` / `.trae` / `.vscode`。
**为什么跳过 `scratch`**：`inbox/scratch/` 是工作空间的**临时产物根**（2026-09-28 起取代 `/tmp/ai4r/`，见 `ai/rules.md` §执行与清理纪律第 1 条）——里面放的是 PDF 解压文本、下载的 tarball、子代理缓存等**中间产物**，本就不是知识树内容，且会被 .gitignore 忽略。
**为什么跳过 `archive`**：该目录按工作空间约定「默认不加载」，其中的历史方案记录的是重构**前**
的路径（如 `projects/diffusiondrive/`），相对链接失效属预期，且各文件头已声明。
若把 archive 计入，其固定 8 条死链会永久淹没真正的新死链 —— 排除后「死链 0」才有信号意义。
**为什么跳过 `.trae`**：那是 IDE 产物（计划文件、skill），不属于工作空间知识树，
其正文按仓库根书写路径（如 `projects/...`），与本检查器「相对当前文件」的口径不同。
**弱引用检查额外豁免 `raw/`**：检索日志的唯一正当入口就是 `sources.md` 的登记行。
**孤儿检查额外豁免 `inbox/`**（2026-09-30 加）：那是支线会话的**转运区**，投递物在被主线程整合前
**本就不该有入链**（见 `ai/rules.md` §支线协作纪律）。若不豁免，"支线只投递、不改共享索引"与
"孤儿必须为 0"两条规则会互相打架——支线要么违规去改共享索引，要么让这项检查永久报红。
**链接扫描跳过两类"假链接"**：``` 围栏代码块（模板示例）与**行内代码跨度** `` `[x](y)` ``（写文档时举例说明链接写法）。
"""
import os, re, sys, csv, subprocess

ROOT = "/home/verse/dev/AI4R"
SKIP_DIRS = {".git", "repos", "scratch", "__pycache__", "node_modules", "archive", ".trae", ".vscode"}

link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# 同上，但同时取出**链接文字**（分册引用归属检查要用文字里的 §X）
link_text_re = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
# 行内代码跨度（`...` / ``...``）：里面的 `[x](y)` 是**举例**，不是真链接。
# 2026-09-24 第二十九轮补：此前只跳围栏代码块，导致"写文档时举例说明链接写法"被误报死链。
# 只认 1~2 个反引号的行内跨度；**3 个及以上整段跳过**（那是 ``` 围栏或正文里提"三反引号"），
# 否则 ``` 会被拆成 2+1 而把配对关系错位，反而漏掉真正的跨度。
code_span_re = re.compile(r"(`{1,2})(?!`)(?:(?!\1).)*?\1(?!`)")


def strip_code(line: str) -> str:
    return code_span_re.sub("", line)

md_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for f in filenames:
        if f.endswith(".md"):
            md_files.append(os.path.join(dirpath, f))

dead = []
for path in md_files:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        in_fence = False
        for lineno, line in enumerate(fh, 1):
            # 跳过 ``` 围栏代码块——里面的链接与表格都是示例，不是真链接
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in link_re.findall(strip_code(line)):
                t = target.strip()
                if t.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                t = t.split("#")[0]
                if not t:
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), t))
                if not os.path.exists(resolved):
                    dead.append((os.path.relpath(path, ROOT), lineno, target))

print(f"扫描 {len(md_files)} 个 md 文件")
print(f"死链: {len(dead)}")
for p, n, t in dead:
    print(f"  {p}:{n} -> {t}")

print("\n--- 行数预算（index.md / state.md 应 <=100）---")
line_budget_over = []
for p in md_files:
    base = os.path.basename(p)
    if base in ("index.md", "state.md"):
        with open(p, encoding="utf-8", errors="ignore") as fh:
            n = sum(1 for _ in fh)
        flag = "  <== 超限" if n > 100 else ""
        if n > 100:
            line_budget_over.append(f"{os.path.relpath(p, ROOT)}: {n} 行")
        print(f"  {os.path.relpath(p, ROOT)}: {n} 行{flag}")
# 第七十八轮：行数超限此前只打印、不进 exit（state.md 涨到 150 行仍全绿）——现并入失败条件。

# ---- 表格单元格数检查（2026-09-24 新增）----
# 起因：一次审计发现表格里有"少一格"的行（渲染会错位）与"单元格内未转义的 |"（会把一列劈成两列），
# 而此前只查死链与行数，这类问题从未被发现。
sep_re = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def _cells(line: str) -> int:
    """数单元格数：先把转义竖线 \\| 换成占位符，再按 | 切。"""
    return len(line.replace("\\|", "\x00").split("|")) - 2


bad_tables = []
for path in md_files:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        lines = fh.read().split("\n")
    # 先剔除围栏代码块内的行（把 ``` 之间的行替换成空串，保持行号不变）
    in_fence = False
    for k, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            in_fence = not in_fence
            lines[k] = ""
            continue
        if in_fence:
            lines[k] = ""
    i = 0
    while i < len(lines):
        # 表格块起点：本行以 | 开头，且下一行是分隔行
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and sep_re.match(lines[i + 1]):
            ncol = _cells(lines[i])
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                n = _cells(lines[j])
                if n != ncol:
                    bad_tables.append((os.path.relpath(path, ROOT), j + 1, ncol, n))
                j += 1
            i = j
        else:
            i += 1

print(f"\n--- 表格单元格数（应为表头列数；转义竖线已处理）---")
print(f"不匹配行: {len(bad_tables)}")
for p, n, ncol, got in bad_tables:
    print(f"  {p}:{n}  表头 {ncol} 列、本行 {got} 格")

# ---- 引用可达性检查（2026-09-24 新增）----
# 起因：一次审计发现 19 篇笔记"只被 sources.md 引用"——读论文表的人看不到这些论文有全文笔记。
# 规则：一个文件应被**至少一个非索引文件**引用；只被 sources.md 引用的算"弱引用"，报警告。
# **豁免 `raw/`**：该目录放的是检索日志/原始取证记录，其唯一正当入口就是 `sources.md` 的登记行，
# 不要求任何论文表或脉络反向链接。若把 raw 计入，其固定 2 条弱引用会永久淹没真正的新弱引用
# —— 与死链检查豁免 `archive` 同理。
INDEX_ONLY = {"sources.md"}
WEAK_EXEMPT_DIRS = ("raw",)
# 孤儿检查豁免的目录。`inbox/` 是支线会话的转运区：投递物在被主线程整合前不应有入链，
# 否则"支线只投递、不改共享索引"与"孤儿必须为 0"两条规则会互相打架（2026-09-30 加）。
ORPHAN_EXEMPT_DIRS = ("inbox",)
refs = {}
for path in md_files:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        in_fence = False
        for line in fh:
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in link_re.findall(strip_code(line)):
                t = target.strip().split("#")[0]
                if not t or t.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), t))
                refs.setdefault(resolved, set()).add(path)

orphan, weak, exempt, orphan_exempt = [], [], 0, 0
for path in md_files:
    srcs = {s for s in refs.get(os.path.normpath(path), set())
            if os.path.normpath(s) != os.path.normpath(path)}
    parts = set(os.path.relpath(path, ROOT).split(os.sep))
    if not srcs:
        if parts & set(ORPHAN_EXEMPT_DIRS):
            orphan_exempt += 1
        else:
            orphan.append(os.path.relpath(path, ROOT))
    elif all(os.path.basename(s) in INDEX_ONLY for s in srcs):
        if parts & set(WEAK_EXEMPT_DIRS):
            exempt += 1
        else:
            weak.append(os.path.relpath(path, ROOT))

print(f"\n--- 引用可达性 ---")
print(f"完全无引用（孤儿）: {len(orphan)}")
for p in orphan:
    print(f"  {p}")
print(f"只被 sources.md 引用（弱引用，应补论文表/脉络里的指针）: {len(weak)}")
for p in weak:
    print(f"  {p}")
print(f"（已豁免 raw/ 检索日志 {exempt} 篇、inbox/ 投递物 {orphan_exempt} 篇）")

# ---- shared/index.md 完整性检查（2026-10-01 第七十九轮新增，第 14 项）----
# 起因：`shared/index.md` 是 shared/ 的目录页，但完整性一直靠手工维护——新增一个 shared/*.md
# 却忘了登记，不会有任何警报（与 README 轮次表漏行同类）。
# 规则：`shared/` **根**下每个 `.md`（`index.md` 自身除外）必须被 `shared/index.md` 链接。
shared_dir = os.path.join(ROOT, "shared")
shared_index = os.path.join(shared_dir, "index.md")
shared_issues = []
if os.path.exists(shared_index):
    _idx_links = set()
    with open(shared_index, encoding="utf-8", errors="ignore") as fh:
        for _t in link_re.findall(strip_code(fh.read())):
            _tt = _t.strip().split("#")[0]
            if _tt and not _tt.startswith(("http", "mailto:")):
                _idx_links.add(os.path.normpath(os.path.join(shared_dir, _tt)))
    for _f in sorted(os.listdir(shared_dir)):
        _p = os.path.join(shared_dir, _f)
        if os.path.isfile(_p) and _f.endswith(".md") and _f != "index.md" and _p not in _idx_links:
            shared_issues.append(f"shared/{_f} 未被 shared/index.md 链接")

print("\n--- shared/index.md 完整性（第 14 项）---")
print(f"未登记: {len(shared_issues)}")
for c in shared_issues:
    print(f"  {c}")

# ---- 分册引用归属检查（2026-09-24 新增）----
# 起因：拆册后正文引用没跟着改册，**这类坑已踩两次**——第二十八轮 C003 的 §I–§P 共 52 处，
# 第三十轮 C005 的 §K–§M 共 13 处。死链检查抓不到（文件确实存在），只有"章节归属"能抓。
# 规则：链接指向 `X.md` 时，链接文字里的 `§X` 必须**存在于 `X.md` 里**；若只在 `X-2.md` 里 → 报错。
# **第四十五轮扩为"可达性"**：原实现只查 `<name>.md ↔ <name>-2.md` 这种**同 basename 的册对**，
# 而 `vla/papers.md` 的 §5–§14 是拆到 **`verification.md` / `verification-2.md`**（换了 basename）
# → 册对逻辑完全看不见，实测留下 **17 处悬空引用**（`papers.md §5…§14`）。
# 现规则：§X 不在目标文件 → 若在它的**册兄弟**里报"错册"，否则报"目标文件里没有该节"。
head_re = re.compile(r"^#{2,3}\s*§?\s*([A-Z]|\d+)(?:[.、]|\s*$)")
sec_cache = {}


def sections(path):
    if path not in sec_cache:
        out = set()
        with open(path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                m = head_re.match(line)
                if m:
                    out.add(m.group(1))
        sec_cache[path] = out
    return sec_cache[path]


def sibling_of(path):
    """返回同 basename 的册兄弟（`X.md` ↔ `X-2.md`），没有则 None。"""
    if path.endswith("-2.md"):
        sib = path[:-5] + ".md"
    else:
        sib = path[:-3] + "-2.md"
    return sib if os.path.exists(sib) else None


pairs = []
for p in md_files:
    if not p.endswith("-2.md") and os.path.exists(p[:-3] + "-2.md"):
        pairs.append((p, p[:-3] + "-2.md"))

bad_vol = []
for path in md_files:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        in_fence = False
        for n, line in enumerate(fh, 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for text, target in link_text_re.findall(strip_code(line)):
                t = target.strip().split("#")[0]
                if not t or t.startswith(("http", "mailto:")):
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), t))
                toks = re.findall(r"§([A-Z]|\d+(?:\.\d+)*)", text)
                if not toks:
                    continue
                if not os.path.exists(resolved):      # 死链由第一项报，这里不重复
                    continue
                here = sections(resolved)
                sib = sibling_of(resolved)
                there = sections(sib) if sib else set()
                for tok in toks:
                    head = tok.split(".")[0]           # `§7.2` 只看主节号 `7`
                    if tok in here or head in here:
                        continue
                    if tok in there or head in there:
                        bad_vol.append((os.path.relpath(path, ROOT), n, f"§{tok}",
                                        f"实际在 {os.path.relpath(sib, ROOT)}"))
                    else:
                        bad_vol.append((os.path.relpath(path, ROOT), n, f"§{tok}",
                                        f"{os.path.relpath(resolved, ROOT)} 里没有这一节"))

print(f"\n--- 章节引用可达性（链接文字里的 §X 必须在目标文件里；含分册归属）---")
print(f"分册对 {len(pairs)} 组，不可达的章节引用: {len(bad_vol)}")
for rel, n, tok, why in bad_vol:
    print(f"  {rel}:{n}  [{tok}]  {why}")

# ---- 笔记「对本项目的意义」节检查（2026-09-24 新增）----
# 起因：47 篇笔记里这一节有 **7 种命名**（对本项目的意义 / 用途 / 与本项目的关系 /
# 与 DiffusionDrive 的关系 / 迁移到自动驾驶（AI 判断）…），其中 5 篇还只写成"在脉络"节里的
# **粗体 bullet**（`- **对本项目的含义**：`）→ 读者与 AI 都定位不到，也无法自动检查。
# 规则：每篇 `notes/*.md` 必须有以 `## 对本项目的意义` 开头的二级标题（允许后缀括注，如"（关键）"）。
# 依据：ai/templates.md 已把该节定为**必写**。
note_sec_re = re.compile(r"^##\s*对本项目的意义")
missing_note_sec = []
for path in md_files:
    if "notes" not in path.split(os.sep):
        continue
    with open(path, encoding="utf-8", errors="ignore") as fh:
        if not any(note_sec_re.match(l) for l in fh):
            missing_note_sec.append(os.path.relpath(path, ROOT))

n_notes = sum(1 for p in md_files if "notes" in p.split(os.sep))
print(f"\n--- 笔记「对本项目的意义」节（必写，见 templates.md）---")
print(f"笔记 {n_notes} 篇，缺该节: {len(missing_note_sec)}")
for p in missing_note_sec:
    print(f"  {p}")

# ---- 小方向 README 的必写节检查（2026-09-24 新增）----
# 起因：`templates.md` 声称的"小方向 README 实际写法"实测**只有 2/6 成立**——
# AD 侧 `vla` / `world-model` 完全符合，而**研究对象 `diffusion-planner` 与具身侧 3 个都缺节**
# （研究对象那个反而最薄：缺"为什么关注 / 要回答的问题 / 已知线索 / 产出状态"）。
# 规则：`topics/<x>/README.md` 必须含「必写 4 节」（节名固定，见 ai/templates.md）。
REQUIRED_TOPIC_SECTIONS = ("本小方向的文件", "要回答的问题", "边界", "产出状态")
missing_topic_sec = []
for path in md_files:
    parts = path.split(os.sep)
    if "topics" not in parts:
        continue
    ti = parts.index("topics")
    if len(parts) != ti + 3 or parts[-1] != "README.md":   # 只认 topics/<x>/README.md
        continue
    with open(path, encoding="utf-8", errors="ignore") as fh:
        heads = {l.strip() for l in fh if l.startswith("## ")}
    miss = [s for s in REQUIRED_TOPIC_SECTIONS if f"## {s}" not in heads]
    if miss:
        missing_topic_sec.append((os.path.relpath(path, ROOT), miss))

n_topics = sum(1 for p in md_files
               if "topics" in p.split(os.sep)
               and len(p.split(os.sep)) == p.split(os.sep).index("topics") + 3
               and p.endswith("README.md"))
print(f"\n--- 小方向 README 的必写 4 节（本小方向的文件 / 要回答的问题 / 边界 / 产出状态）---")
print(f"小方向 {n_topics} 个，缺节: {len(missing_topic_sec)}")
for p, miss in missing_topic_sec:
    print(f"  {p}  缺: {'、'.join(miss)}")

# ---- 判断条数一致性检查（2026-09-24 新增）----
# 起因：第四十四轮发现 `judgments.md` 的 D 组**实际只有 10 条 bullet，而节标题、索引表、state.md 都写 11**
# ——一条第十七轮的判断（DIVER 的 `num_cmd` 口径）在某轮编辑中被**静默删掉**，因为没有任何一项检查
# 对比"声明的条数"与"实际的 bullet 数"。计数是这类文档的**承重信息**（ai/workflows.md §轮次收尾第 6 条：
# "引用可以重复，计数不能"），必须有机器检查。
# 规则：以**实际 bullet 数**为唯一权威，比对三处声明——① 节标题 `### X. 标题（N 条）`
# ② `judgments.md` 分组索引表的"条数"列（并核对该行"册"列与本节实际所在册）
# ③ `state.md` 判断边界索引表的"条数"列与总条数（"**N 条判断的完整论证"）。
GROUP_HEAD_RE = re.compile(r"^###\s+([A-H])\.\s+(.*?)(?:（(\d+)\s*条）)?\s*$")
IDX_ROW_RE = re.compile(r"^\|\s*\*\*([A-H])\*\*\s*\|([^|]*)\|([^|]*)\|([^|]*)\|")
STATE_ROW_RE = re.compile(r"^\|\s*\*\*([A-H])\*\*\s*\|([^|]*)\|([^|]*)\|\s*$")

count_issues = []
for vol_path in md_files:
    base = os.path.basename(vol_path)
    if not re.fullmatch(r"judgments(-\d+)?\.md", base):
        continue
    pdir = os.path.dirname(vol_path)
    with open(vol_path, encoding="utf-8", errors="ignore") as fh:
        lines = fh.read().split("\n")
    # ① 本节实际 bullet 数 vs 节标题声明
    actual, declared_hdr, cur = {}, {}, None
    for l in lines:
        m = GROUP_HEAD_RE.match(l)
        if m:
            cur = m.group(1)
            actual[cur] = 0
            if m.group(3):
                declared_hdr[cur] = int(m.group(3))
            continue
        if cur and l.startswith("- "):
            actual[cur] += 1
    for g in actual:
        if g in declared_hdr and declared_hdr[g] != actual[g]:
            count_issues.append(f"{os.path.relpath(vol_path, ROOT)} §{g} 节标题写 {declared_hdr[g]} 条、实际 {actual[g]} 条")
        elif g not in declared_hdr:
            count_issues.append(f"{os.path.relpath(vol_path, ROOT)} §{g} 节标题未写条数（实际 {actual[g]} 条）")
    # ② judgments.md 分组索引表：条数 + 册别
    if base == "judgments.md":
        with open(vol_path, encoding="utf-8", errors="ignore") as fh:
            for n, l in enumerate(fh, 1):
                m = IDX_ROW_RE.match(l)
                if not m:
                    continue
                g, cnt, vol = m.group(1), m.group(3).strip(), m.group(4).strip()
                if not cnt.isdigit():
                    continue
                if g in actual and int(cnt) != actual[g]:
                    count_issues.append(f"{os.path.relpath(vol_path, ROOT)}:{n} 索引表 §{g} 写 {cnt} 条、实际 {actual[g]} 条")
        # 册列正确性：§X 实际在哪个文件里
        sib = os.path.join(pdir, "judgments-2.md")
        if os.path.exists(sib):
            with open(sib, encoding="utf-8", errors="ignore") as fh:
                vol2_groups = {m.group(1) for m in (GROUP_HEAD_RE.match(l) for l in fh) if m}
            with open(vol_path, encoding="utf-8", errors="ignore") as fh:
                for n, l in enumerate(fh, 1):
                    m = IDX_ROW_RE.match(l)
                    if not m:
                        continue
                    g, vol = m.group(1), m.group(4).strip()
                    if not vol:
                        continue
                    in_first, in_second = g in actual, g in vol2_groups
                    if vol == "第一册" and in_second and not in_first:
                        count_issues.append(f"{os.path.relpath(vol_path, ROOT)}:{n} 索引表 §{g} 标「第一册」但实际在第二册")
                    if vol == "第二册" and in_first and not in_second:
                        count_issues.append(f"{os.path.relpath(vol_path, ROOT)}:{n} 索引表 §{g} 标「第二册」但实际在第一册")
        # ③ state.md 索引表 + 总条数
        st = os.path.join(pdir, "state.md")
        if os.path.exists(st):
            total_actual = sum(actual.values())
            if os.path.exists(sib):
                with open(sib, encoding="utf-8", errors="ignore") as fh:
                    in_grp = False
                    for l in fh:
                        if GROUP_HEAD_RE.match(l):
                            in_grp = True
                            continue
                        if in_grp and l.startswith("- "):
                            total_actual += 1
            with open(st, encoding="utf-8", errors="ignore") as fh:
                for n, l in enumerate(fh, 1):
                    m = STATE_ROW_RE.match(l)
                    if m:
                        g, cnt = m.group(1), m.group(3).strip()
                        if cnt.isdigit() and g in actual and int(cnt) != actual[g]:
                            count_issues.append(f"{os.path.relpath(st, ROOT)}:{n} 索引表 §{g} 写 {cnt} 条、实际 {actual[g]} 条")
                    mt = re.search(r"\*\*(\d+)\s*条判断", l)
                    if mt and int(mt.group(1)) != total_actual:
                        count_issues.append(f"{os.path.relpath(st, ROOT)}:{n} 写总条数 {mt.group(1)}、实际 {total_actual} 条")

print(f"\n--- 判断条数一致性（实际 bullet 数为准，比对节标题 / judgments.md 索引表 / state.md 索引表）---")
print(f"不一致: {len(count_issues)}")
for c in count_issues:
    print(f"  {c}")

# ---- 声明计数 vs 权威源检查（2026-09-24 第四十四轮新增）----
# 起因：`state.md` 与 `sources.md` 都写"`transfer.md` 16 条机制"，而 §1 实际只有 **15** 条——
# 第三十二轮把条数改正为 15 时**只改了 `preparation.md` 那处**，兄弟引用漏改，一年也没人发现。
# 这与第八项是**同一类病**（计数与内容脱钩），只是权威源在"文档之外"（目录数、表格行数、编号数）。
# 设计：一张**显式登记表**（下方 `COUNT_RULES`）——每条 = ① 权威源怎么数 ② 声明写在哪个文件的哪个模式里。
# 之所以要显式登记：机器无法从"16 条机制"这句话推出它数的是哪张表。代价是**措辞改了要更新登记表**——
# 因此"声明处没匹配到"也**报出来**（那是信号：文档被改写，登记表该更新），而不是静默通过。
COUNT_RULES = []


def _uniq_ids(path, pat):
    """数一个文件里出现的、去重后的编号（如 VLA-01…VLA-28）。"""
    if not os.path.exists(path):
        return None
    return len(set(re.findall(pat, open(path, encoding="utf-8", errors="ignore").read())))


def _repo_dirs():
    d = os.path.join(ROOT, "projects/autonomous-driving/code/repos")
    if not os.path.isdir(d):
        return None
    return sum(1 for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))


def _transfer_sec1_rows():
    p = os.path.join(ROOT, "projects/autonomous-driving/topics/diffusion-planner/transfer.md")
    if not os.path.exists(p):
        return None
    n, inside = 0, False
    for l in open(p, encoding="utf-8", errors="ignore"):
        if l.startswith("## 1."):
            inside = True
            continue
        if inside and l.startswith("### 1.1"):
            break
        if inside and l.startswith("| "):
            n += 1
    return max(n - 1, 0)          # 减表头（分隔行 `|---|` 不以 `| ` 开头，未计入）


def _rounds_volumes():
    """数 history 目录下的卷文件数（权威源）。"""
    d = os.path.join(ROOT, "projects/autonomous-driving/history")
    if not os.path.isdir(d):
        return None
    return sum(1 for x in os.listdir(d) if re.fullmatch(r"rounds-.+\.md", x))


# 起因（2026-10-01 第七十六轮）：卷数**连续两次差 1**——第六十七轮发现声明"47 卷"而实际 48；
# 第七十六轮又发现声明"57 卷"而实际 **58**。**同一个派生值手写三处、权威源在"文件数"**，
# 正是第九项要治的病，却一直没登记。→ 本轮把它并入登记表。
COUNT_RULES += [
    ("history 卷数", _rounds_volumes, [
        ("projects/autonomous-driving/history.md", r"## 分卷（共 (\d+) 卷）"),
        ("projects/autonomous-driving/index.md", r"索引 \+ (\d+) 卷正文"),
        ("projects/autonomous-driving/state.md", r"共 (\d+) 卷，"),
        ("projects/autonomous-driving/state.md", r"\[history\.md\]\(history\.md\)（索引 \+ (\d+) 卷，"),
        ("README.md", r"索引 \+ (\d+) 卷）为准"),
    ]),
]

COUNT_RULES += [
    ("仓库快照数", _repo_dirs, [
        ("projects/autonomous-driving/state.md", r"\*\*(\d+) 个官方仓库快照"),
        ("projects/autonomous-driving/index.md", r"官方代码快照清单（\*\*(\d+) 个仓库"),
    ]),
    ("VLA 论文篇数", lambda: _uniq_ids(os.path.join(ROOT, "projects/autonomous-driving/topics/vla/papers.md"),
                                     r"VLA-\d+"), [
        ("projects/autonomous-driving/state.md", r"\[VLA \*\*(\d+)\*\* 篇\]"),
        ("projects/autonomous-driving/index.md", r"\[论文表 \*\*(\d+) 篇\*\*\]\(topics/vla/papers.md\)"),
    ]),
    ("世界模型论文篇数", lambda: _uniq_ids(os.path.join(ROOT, "projects/autonomous-driving/topics/world-model/papers.md"),
                                       r"WM-\d+"), [
        ("projects/autonomous-driving/state.md", r"世界模型 (\d+) 篇\]"),
        ("projects/autonomous-driving/index.md", r"\[论文表 \*\*(\d+) 篇\*\*\]\(topics/world-model/papers.md\)"),
    ]),
    ("研究对象论文篇数（DP-A）", lambda: _uniq_ids(
        os.path.join(ROOT, "projects/autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad.md"),
        r"DP-A\d+"), [
        ("projects/autonomous-driving/state.md", r"DP-A01–A(\d+)"),
        ("projects/autonomous-driving/index.md", r"DP-A01–A(\d+)"),
    ]),
    ("E2E 综述篇数（S）", lambda: _uniq_ids(
        os.path.join(ROOT, "projects/autonomous-driving/direction/surveys/e2e_ad_surveys.md"), r"\bS\d{3}\b"), [
        ("projects/autonomous-driving/state.md", r"S001–S(\d+)"),
        ("projects/autonomous-driving/index.md", r"S001–S(\d+)"),
    ]),
    ("笔记篇数", lambda: n_notes, [
        ("projects/autonomous-driving/state.md", r"\| 笔记 \| (\d+) 篇"),
    ]),
    ("transfer.md §1 机制条数", _transfer_sec1_rows, [
        ("projects/autonomous-driving/state.md", r"§1 现 (\d+) 条"),
        ("projects/autonomous-driving/sources.md", r"§1 现 (\d+) 条"),
    ]),
]

# 平级项目 `embodied-ai` 的同类计数（2026-09-24 第四十四轮同批补齐）——两个项目的规矩相同，
# 机器检查也应覆盖，否则"只查了主项目"本身就是一个盲区。
EMB = os.path.join(ROOT, "projects/embodied-ai")


def _notes_under(needle):
    return sum(1 for p in md_files if "notes" in p.split(os.sep) and needle in p)


def _emb_summary_level_rows():
    """数具身侧 DP-E 表里"摘要级"的条数——口径：证据状态含「摘要」且**不含**「全文」。
    注意该表有"多行条目"写法（续行的 ID 单元格为空），必须按 ID 非空过滤，否则会多算。"""
    p = os.path.join(EMB, "topics/diffusion-policy/papers/diffusion_planner_embodied.md")
    if not os.path.exists(p):
        return None
    lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
    n, i = 0, 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|") and "证据状态" in l:
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                cells = [x.strip() for x in lines[j].strip("|").split("|")]
                if cells[0].startswith("DP-E"):
                    ev = cells[-1]
                    if "摘要" in ev and "全文" not in ev:
                        n += 1
                j += 1
            i = j
        else:
            i += 1
    return n


COUNT_RULES += [
    ("具身·扩散策略篇数（DP-E）", lambda: _uniq_ids(
        os.path.join(EMB, "topics/diffusion-policy/papers/diffusion_planner_embodied.md"), r"DP-E\d+"), [
        ("projects/embodied-ai/state.md", r"DP-E01–E(\d+)"),
        ("projects/embodied-ai/index.md", r"DP-E01–E(\d+)"),
        ("projects/embodied-ai/topics/diffusion-policy/README.md", r"\*\*在表 (\d+) 篇\*\*"),
    ]),
    ("具身·VLA 篇数", lambda: _uniq_ids(os.path.join(EMB, "topics/vla/papers.md"), r"E-VLA-\d+"), [
        ("projects/embodied-ai/state.md", r"\[VLA (\d+) 篇\]"),
        ("projects/embodied-ai/index.md", r"：(\d+) 篇（\[papers\.md\]\(topics/vla/papers\.md\)）"),
        ("projects/embodied-ai/topics/vla/README.md", r"\*\*在表 (\d+) 篇\*\*"),
    ]),
    ("具身·世界模型篇数", lambda: _uniq_ids(os.path.join(EMB, "topics/world-model/papers.md"), r"E-WM-\d+"), [
        ("projects/embodied-ai/state.md", r"世界模型 (\d+) 篇\]"),
        ("projects/embodied-ai/index.md", r"：(\d+) 篇（\[papers\.md\]\(topics/world-model/papers\.md\)）"),
        ("projects/embodied-ai/topics/world-model/README.md", r"\*\*在表 (\d+) 篇\*\*"),
    ]),
    ("具身·扩散策略笔记篇数", lambda: _notes_under(os.sep + "embodied-ai" + os.sep), [
        ("projects/embodied-ai/state.md", r"\| 笔记 \| (\d+) 篇"),
        ("projects/embodied-ai/topics/diffusion-policy/README.md", r"\*\*(\d+) 篇有全文笔记\*\*"),
    ]),
    ("具身·DP-E 摘要级条数", _emb_summary_level_rows, [
        ("projects/embodied-ai/state.md", r"\*\*(\d+) 条摘要级\*\*"),
        ("projects/embodied-ai/state.md", r"\*\*有 (\d+) 条为摘要级\*\*"),
        ("projects/embodied-ai/index.md", r"\*\*其中 (\d+) 条摘要级\*\*"),
    ]),
]

def _scoring_line_sec2_bullets():
    """数 scoring_line.md §二（线索级）的条目数——口径：`## 二、` 起至下一个 `## ` 节之间 `- ` 开头的行。"""
    p = os.path.join(ROOT, "projects/autonomous-driving/topics/diffusion-planner/papers/scoring_line.md")
    if not os.path.exists(p):
        return None
    n, inside = 0, False
    for l in open(p, encoding="utf-8", errors="ignore"):
        if l.startswith("## 二、"):
            inside = True
            continue
        if inside and l.startswith("## "):
            break
        if inside and l.startswith("- "):
            n += 1
    return n


def _pdfs_pending_rows():
    """数 pdfs_pending.md A 节（需用户协助下载）的表行——口径：`## A.` 起至下一 `## ` 节之间 `| P` 开头的行。"""
    p = os.path.join(ROOT, "projects/autonomous-driving/pdfs_pending.md")
    if not os.path.exists(p):
        return None
    n, inside = 0, False
    for l in open(p, encoding="utf-8", errors="ignore"):
        if l.startswith("## A."):
            inside = True
            continue
        if inside and l.startswith("## "):
            break
        if inside and l.startswith("| P"):
            n += 1
    return n


# 起因（2026-10-01 第七十七轮巡查补盲）：三处"声明计数"此前未登记——scoring_line 的"17 条线索级"
# 实际只有 15 条（漂移一直无人发现，正是第九项要治的病却没登记）、pdfs_pending 的 8 条、
# navhard 竞品的 DP-C01–C07。
COUNT_RULES += [
    ("选优器专线·线索级条数", _scoring_line_sec2_bullets, [
        ("projects/autonomous-driving/state.md", r"§二 (\d+) 条线索级"),
        ("projects/autonomous-driving/index.md", r"已核 \+ (\d+) 条线索级"),
        ("projects/autonomous-driving/ideas/sota-plan.md", r"§二另有 \*\*(\d+) 条线索级\*\*"),
    ]),
    ("待下载 PDF 条数", _pdfs_pending_rows, [
        ("README.md", r"付费墙 PDF（\*\*(\d+) 条\*\*）"),
        ("projects/autonomous-driving/state.md", r"(\d+) 篇付费墙 PDF"),
        ("projects/autonomous-driving/index.md", r"付费墙 PDF (\d+) 条"),
    ]),
    ("navhard 竞品条数（DP-C）", lambda: _uniq_ids(
        os.path.join(ROOT, "projects/autonomous-driving/topics/diffusion-planner/papers/navhard_competitors.md"),
        r"DP-C\d+"), [
        ("projects/autonomous-driving/index.md", r"DP-C01–C(\d+)"),
    ]),
]

count2_issues = []
for label, source, decls in COUNT_RULES:
    actual = source()
    if actual is None:
        count2_issues.append(f"{label}：权威源不存在（{source.__name__ if hasattr(source,'__name__') else '?'}）")
        continue
    for rel, rx in decls:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            count2_issues.append(f"{label}：声明处文件不存在 {rel}")
            continue
        m = re.search(rx, open(p, encoding="utf-8", errors="ignore").read())
        if not m:
            count2_issues.append(f"{label}：{rel} 里未找到声明（措辞可能已改，请更新 check_links.py 的登记表）")
        elif int(m.group(1)) != actual:
            count2_issues.append(f"{label}：{rel} 写 {int(m.group(1))}、权威源实际 {actual}")

print(f"\n--- 声明计数 vs 权威源（{len(COUNT_RULES)} 条规则；权威源 = 目录数 / 表格编号数 / 笔记文件数 / §1 行数）---")
print(f"不一致: {len(count2_issues)}")
for c in count2_issues:
    print(f"  {c}")

# ---- CSV 与 markdown 表的 ID 一致性检查（2026-09-24 第四十六轮新增）----
# 依据：工作空间约定「CSV 是与 markdown 表**双表示**时的权威源」（见 workspace-design.md 与各论文表文件头）。
# 但"谁是权威"只在两者一致时才有意义——**一旦漂移，按 md 读的人与按 CSV 检索的人会看到两个不同的集合**，
# 而且两边都"看起来对"。这类漂移没有任何现有检查能发现（死链、计数、章节都管不到）。
# 规则：对每一对 `<x>.csv` + `<x>.md`，**两边出现的 ID 集合必须完全相同**（双向都报）。
# 为什么扫"全单元格"而不是"ID 列"：各 CSV 的列布局不同（`e2e_ad_surveys` 的 ID 在第 1 列且表头小写 `id`，
# 其余三张在第 2/5 列），且**待核验 / 边界外**的条目在 CSV 里是"段标题行 + 别的列"，只扫 ID 列会漏。
# 实测（第四十六轮）：4 对**全部一致**（45 / 34 / 15 / 28，双向零差）——本项是**把已有的正确状态锁住**。
CSV_ID_PAIRS = [
    ("projects/autonomous-driving/direction/surveys/e2e_ad_surveys", r"S\d{3}"),
    ("projects/autonomous-driving/topics/diffusion-planner/papers/diffusion_planner_ad", r"DP-A\d+"),
    ("projects/autonomous-driving/topics/diffusion-planner/surveys/diffusion_planner_surveys", r"DP-S\d+"),
    ("projects/embodied-ai/topics/diffusion-policy/papers/diffusion_planner_embodied", r"DP-E\d+"),
]

csv_issues = []
for base, pat in CSV_ID_PAIRS:
    cp, mp = os.path.join(ROOT, base + ".csv"), os.path.join(ROOT, base + ".md")
    if not os.path.exists(cp):
        csv_issues.append(f"{base}.csv 不存在")
        continue
    if not os.path.exists(mp):
        csv_issues.append(f"{base}.md 不存在")
        continue
    rx = re.compile(pat)
    with open(cp, encoding="utf-8", errors="ignore") as fh:
        csv_ids = {c.strip() for row in csv.reader(fh) for c in row if rx.fullmatch(c.strip())}
    with open(mp, encoding="utf-8", errors="ignore") as fh:
        # 第七十九轮：与 CSV 端同口径——要求 ID 两侧不是字母数字（此前用 findall，子串也命中）
        md_ids = set(re.findall(r"(?<![0-9A-Za-z])" + pat + r"(?![0-9A-Za-z])", fh.read()))
    only_csv, only_md = sorted(csv_ids - md_ids), sorted(md_ids - csv_ids)
    if only_csv:
        csv_issues.append(f"{os.path.basename(base)}: 只在 CSV → {only_csv}")
    if only_md:
        csv_issues.append(f"{os.path.basename(base)}: 只在 md → {only_md}")

print(f"\n--- CSV 与 markdown 表的 ID 一致性（{len(CSV_ID_PAIRS)} 对；双表示时 CSV 是权威源，两者集合须相同）---")
print(f"不一致: {len(csv_issues)}")
for c in csv_issues:
    print(f"  {c}")

# ---- inbox 待整合检查（2026-09-30 第六十二轮新增，第 11 项；见 ai/rules.md §支线协作纪律）----
# 起因：支线投递物原靠 `workflows.md` §轮次收尾第 9 步的**人工 checklist** 整合，
# **而本工作空间自己的历史证明 checklist 会漏**——第 49–54 轮都漏了收尾第 2/3 步，且**没有任何警报**。
# 把它变成机器检查，才能形成闭环：**不整合，提交就不干净**（第 7 步跑检查 → 第 8 步提交）。
# 规则：`inbox/` **根**下的 `.md`（`cleanup.md` 除外）即"待整合投递物"，非 0 即报。
# **不查子目录**：`inbox/scratch/` 是临时产物根（已被 SKIP_DIRS 跳过），不属于投递物。
# 处置：采纳 / 否决 / 搁置都要移出 `inbox/`（移入 `archive/`），否则本项会永久报警而被无视。
INBOX = os.path.join(ROOT, "inbox")
INBOX_KEEP = {"cleanup.md"}
pending = []
if os.path.isdir(INBOX):
    for _name in sorted(os.listdir(INBOX)):
        _p = os.path.join(INBOX, _name)
        if os.path.isfile(_p) and _name.endswith(".md") and _name not in INBOX_KEEP:
            pending.append(f"inbox/{_name}")

print(f"\n--- inbox 待整合（第 11 项；`cleanup.md` 除外）---")
print(f"待整合投递物: {len(pending)} 篇")
for c in pending:
    print(f"  {c}")

# ---- 投递物已入 git 检查（2026-10-01 第七十九轮新增，第 15 项）----
# 起因：规则要求支线投递物投递后自己提交一次（rules.md §支线协作纪律第 4 条），理由是
# **未被 git 跟踪的内容一旦被覆盖就无法恢复**（本工作空间最痛的一类）。而第 11 项只数个数、
# 不校验是否已入库——未提交的半成品照样"绿灯通过"。
# 规则：每个 `inbox/*.md` 投递物（`cleanup.md` 除外）必须已被 git 跟踪。
untracked = []
for rel in pending:
    _r = subprocess.run(["git", "-C", ROOT, "ls-files", "--error-unmatch", rel],
                        capture_output=True, text=True)
    if _r.returncode != 0:
        untracked.append(f"{rel}（未被 git 跟踪——覆盖后无法恢复）")

print("\n--- 投递物已入 git（第 15 项）---")
print(f"未跟踪: {len(untracked)}")
for c in untracked:
    print(f"  {c}")

# ---- 文档体积预算检查（2026-09-30 第六十四轮新增，第 12 项；第七十四轮加"预警线"）----
# 依据：`ai/rules.md` §文件更新 的尺寸阈值——「**任何文档 ≤ 64 KiB**」，
# 而 64 KiB 是 **Read 工具一次可整读的物理上限**（**第七十四轮实测复证**：整读一个 67 KiB 的文件，
# 工具直接报 `selected content size exceeds the limit of 64KB`）→ **是硬约束、不可上调**。
# 第五十七轮实测 8 表全部达标（最大 DP-A 表 57 KiB）；此条约定曾长期只是人工"看体积"→ 第六十四轮机器化。
# **为什么值得机器化**：超限是**静默**发生的（加一节就跨过去了），后果是"这个文件从此读不整"。
# **两线制（第七十四轮定）**：
#   · 硬线 64 KiB（65536）—— 超 = 违规，参与 exit code，收尾前必须处理；
#   · 预警线 60 KiB（61440）—— 只报不阻断，留约一轮增量余量，避免"下一轮就撞线"（`history.md` 即如此）。
# **超限处理按文件角色分档**（本脚本只认线、不认角色，分档见 `ai/rules.md` §文件更新）：
#   索引/登记类 → 瘦身（详情在别处）；脉络/清单类 → 拆册；决策/交叉引用稠密类 → 优先去重、必要时拆册。
# 只查被扫描的 md（已排除 code/repos、archive、inbox/scratch、.trae）。
LIMIT_BYTES = 64 * 1024
WARN_BYTES = 60 * 1024
oversize = []
warnsize = []
for path in md_files:
    sz = os.path.getsize(path)
    if sz > LIMIT_BYTES:
        oversize.append(f"{os.path.relpath(path, ROOT)}  {sz} 字节（{sz / 1024:.1f} KiB，超 {sz - LIMIT_BYTES} 字节）")
    elif sz > WARN_BYTES:
        warnsize.append(f"{os.path.relpath(path, ROOT)}  {sz} 字节（{sz / 1024:.1f} KiB，距硬线还差 {LIMIT_BYTES - sz} 字节）")

print(f"\n--- 文档体积预算（第 12 项；硬线 {LIMIT_BYTES} 字节 = 64 KiB，预警线 {WARN_BYTES} 字节 = 60 KiB）---")
print(f"超限（违规）: {len(oversize)}")
for c in oversize:
    print(f"  {c}")
print(f"预警（距硬线 < 4 KiB）: {len(warnsize)}")
for c in warnsize:
    print(f"  {c}")
if md_files and not oversize and not warnsize:
    _big = max(md_files, key=os.path.getsize)
    print(f"  最大: {os.path.relpath(_big, ROOT)}  {os.path.getsize(_big)} 字节"
          f"（{os.path.getsize(_big) / 1024:.1f} KiB，占 {os.path.getsize(_big) / LIMIT_BYTES:.0%}）")

# ---- README 轮次表完整性检查（2026-10-01 第七十七轮新增，第 13 项）----
# 起因：第 67/68 轮的收尾漏在 README 轮次指针表加行（第 76 轮只补了「最近动态」）——漏行**不产生死链**
# （rounds-67.md 本身存在、history.md 也链接它），死链/孤儿检查都抓不到，只有"README 链接到的
# 单轮卷号集合"本身能查。规则（两条判定，均在 README.md 全文里取 `rounds-N.md` 的纯数字 N；
# `rounds-24a.md` 与区间卷 `rounds-18-23.md` 天然不匹配正则、不计入）：
#   ① max(README 卷号) == history/ 下实际单轮卷的最大号（最新一卷必须已被 README 链接——
#      「最近动态」与指针表任一处链接即算）；
#   ② README 卷号在 [min, max] 区间内无缺口（漏行即缺口；表尾「更早（第一至N轮）」行收编旧轮后
#      min 上移，缺口判定随之下移，不误报）。
README_MD = os.path.join(ROOT, "README.md")
# 字母后缀（rounds-24a.md / 78a.md）按数字主干归组（78a 记作 78）——第七十八轮放宽：
# 此前正则不认后缀，若某轮只有 78a 卷且为最新，max 判定失明；79 出现后 78 又假阳性缺口。
_round_file_re = re.compile(r"rounds-(\d+)[a-z]?\.md")
readme_rounds = set()
if os.path.exists(README_MD):
    readme_rounds = {int(n) for n in _round_file_re.findall(
        open(README_MD, encoding="utf-8", errors="ignore").read())}
HIST_DIR = os.path.join(ROOT, "projects/autonomous-driving/history")
actual_rounds = set()
if os.path.isdir(HIST_DIR):
    for _f in os.listdir(HIST_DIR):
        _m = _round_file_re.fullmatch(_f)
        if _m:
            actual_rounds.add(int(_m.group(1)))
readme_issues = []
if not actual_rounds:
    readme_issues.append("history/ 下没有单轮卷（rounds-N.md）——第 13 项的前提失效，请核查路径")
elif not readme_rounds:
    readme_issues.append("README.md 未链接任何单轮卷（rounds-N.md）")
else:
    if max(readme_rounds) != max(actual_rounds):
        readme_issues.append(
            f"README 链接的最新单轮卷是 {max(readme_rounds)}、实际最新是 {max(actual_rounds)}——最新一卷未入 README")
    _gaps = [n for n in range(min(readme_rounds), max(readme_rounds) + 1) if n not in readme_rounds]
    if _gaps:
        readme_issues.append(
            f"README 轮次表缺口：区间 {min(readme_rounds)}–{max(readme_rounds)} 内未被链接的轮次 {_gaps}")

print(f"\n--- README 轮次表完整性（第 13 项；单轮卷链接须覆盖最新且无缺口）---")
if readme_rounds:
    print(f"README 链接单轮卷 {len(readme_rounds)} 个（{min(readme_rounds)}–{max(readme_rounds)}），"
          f"实际单轮卷 {len(actual_rounds)} 个（最新 {max(actual_rounds) if actual_rounds else '-'}）")
print(f"不一致: {len(readme_issues)}")
for c in readme_issues:
    print(f"  {c}")

# ---- 轮次 tag 检查（2026-10-01 第七十九轮新增，第 16 项）----
# 起因：规则要求每轮打 annotated tag `round-N`（rules.md §执行与清理纪律第 9 条），否则正文里的
# "见第 N 轮"落不到 `git show round-N`；而 tag 缺失没有任何警报。
roundtag_issues = []
if actual_rounds:
    _N = max(actual_rounds)
    _r = subprocess.run(["git", "-C", ROOT, "tag", "-l", f"round-{_N}"], capture_output=True, text=True)
    if not _r.stdout.strip():
        roundtag_issues.append(f"缺 annotated tag round-{_N}（见 rules.md §执行与清理纪律第 9 条）")

print("\n--- 轮次 tag（第 16 项；最新单轮卷须有 round-N 标签）---")
print(f"不一致: {len(roundtag_issues)}")
for c in roundtag_issues:
    print(f"  {c}")

# ---- 失败分级汇总（第七十八轮加）----
# 阻断级（参与 exit 1）：死链 / 表格错位 / 孤儿 / 章节错册 / 缺必写节 / 判断与声明计数 / CSV / inbox / 超限 / 行数超预算 / README 轮次表。
# 提示级（只报不阻断）：弱引用（#4 的半档）、体积预警（60–64 KiB 预警带）。
# exit 语义不变（防"永久报警被无视"的旧教训）——汇总行只为快速定位该修什么。
_blocking = (len(dead) + len(bad_tables) + len(orphan) + len(bad_vol) + len(missing_note_sec)
             + len(missing_topic_sec) + len(count_issues) + len(count2_issues) + len(csv_issues)
             + len(pending) + len(oversize) + len(line_budget_over) + len(readme_issues)
             + len(shared_issues) + len(untracked) + len(roundtag_issues))
_advisory = len(weak) + len(warnsize)
print(f"\n=== 汇总：阻断 {_blocking} 项 / 提示 {_advisory} 项（提示 = 弱引用 {len(weak)} + 体积预警 {len(warnsize)}；exit 1 当且仅当阻断 > 0）===")

sys.exit(1 if (dead or bad_tables or orphan or bad_vol or missing_note_sec
               or missing_topic_sec or count_issues or count2_issues or csv_issues
               or pending or oversize or line_budget_over or readme_issues
               or shared_issues or untracked or roundtag_issues) else 0)


