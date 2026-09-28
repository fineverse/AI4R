# CCF 推荐国际学术会议和期刊目录（2026 正式版）

结构化数据：`ccf-2026-all.json`（单一事实源）、`ccf-2026-journals.csv`、`ccf-2026-conferences.csv`。
原始 PDF 已归档至 `archive/ccf-2026/`（默认不加载）。

## 来源与抽取

- 来源：《第七版中国计算机学会推荐国际学术会议和期刊目录（2026正式版）.pdf》（72 页，2026 正式版）
- 抽取日期：2026-09-22；解析脚本：`scripts/parse_ccf_2026.py`（纯 stdlib，读 bbox 导出的词级坐标）
- 数据忠实转录 PDF 原文；个别词级坐标重叠的行（CASAXR、EITEE、CVMJ）按原始文本人工核验后修正，见脚本内 `OVERRIDES`

## 统计

- 总计 **681** 条：期刊 **295**，会议 **386**
- 领域（10 个）：计算机体系结构/并行与分布计算/存储系统、计算机网络、网络与信息安全、软件工程/系统软件/程序设计语言、数据库/数据挖掘/内容检索、计算机科学理论、计算机图形学与多媒体、人工智能、人机交互与普适计算、交叉/综合/新兴
- 每个领域内期刊表与会议表各分 A/B/C 三类（`rank` 字段）

## 字段说明

| 字段 | 说明 |
|---|---|
| `area` | 所属领域 |
| `kind` | `journal` 期刊 / `conference` 会议 |
| `rank` | CCF 评级：`A` / `B` / `C` |
| `number` | 该表内序号（1 起，同表内唯一） |
| `abbreviation` | 简称（PDF 原文为空则留空） |
| `full_name` | 全称 |
| `publisher` | 出版社/主办方 |
| `url` | 官网/DBLP 链接；多个链接以空格分隔（如 ECML-PKDD） |
| `aliases` | 原简称/原名（来自「（原 …）」注释，`;` 分隔） |
| `former_publishers` | 原出版社（来自出版社列的「（原 …）」注释） |
| `source_pages` | 在 PDF 中的页码（1 起，`+` 分隔） |

## 按 CCF 评级筛选论文

`ccf-2026-all.json` 为权威副本；CSV 由其生成，改动请先改 JSON 再重生成。

```python
import json
ccf = json.load(open('shared/ccf/ccf-2026-all.json'))

# 常用查找：按简称取评级
by_abbr = {(r['kind'], r['abbreviation'].upper()): r for r in ccf if r['abbreviation']}
def rating(kind, abbr):          # kind: 'conference' / 'journal'
    r = by_abbr.get((kind, abbr.upper()))
    return r['rank'] if r else None

rating('conference', 'CVPR')     # -> 'A'
rating('conference', 'ICLR')     # -> 'A'
rating('journal', 'TPAMI')       # -> 'A'

# 筛出某评级的所有会议/期刊（含别名匹配）
def is_rank(r, kind, *ranks):
    return r['kind'] == kind and r['rank'] in ranks
a_conf = [r for r in ccf if is_rank(r, 'conference', 'A')]
b_c_journals = [r for r in ccf if is_rank(r, 'journal', 'B', 'C')]
```

CSV 用法（pandas）：

```python
import pandas as pd
df = pd.read_csv('shared/ccf/ccf-2026-conferences.csv')
df[df['rank'] == 'A']                                  # 全部 A 类会议
df[(df['area'].str.startswith('人工智能')) & (df['rank'].isin(['A','B']))]
```

## 注意事项

- 2 条记录 PDF 原文无 URL：`JCC`（会议，体系结构 C 类 30 号）、`JATS`（期刊，人工智能 C 类 39 号）
- 部分期刊/会议在 PDF 中无简称（如 Machine Learning、Ad Hoc Networks），`abbreviation` 留空，属原文如此
- `area` 以 PDF 归类为准（如 CVPR/ICCV/ECCV/IJCAI 位于「人工智能」领域）
- `rank` 直接对应 CCF A/B/C 评级；同领域内期刊与会议分别排序
