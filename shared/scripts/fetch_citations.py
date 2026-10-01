#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Semantic Scholar 批量抓取论文元数据（带 429 退避重试）。

为什么需要它：S2 官方 API 的 429 是**间歇性**的，且实测**与请求间隔无强相关**
（6 秒间隔 2/4 成功、10 秒间隔 2/3 成功，批量 7 个 ID 成功而批量 2 个反而失败）
→ 唯一可靠的做法是「失败重试 + 指数退避」，而不是拉长固定间隔。本脚本封装该逻辑。

用法：
    # 从命令行给 ID（支持 DOI / arXiv ID / PMID / S2 ID）
    python3 fetch_citations.py arXiv:2307.15818 arXiv:2406.09246

    # 从文件读（每行一个 ID，# 开头为注释）
    python3 fetch_citations.py --ids-file ids.txt --out citations.tsv

    # 自定义字段
    python3 fetch_citations.py --fields title,year,citationCount < ids.txt

凭据：依次尝试环境变量 S2_API_KEY、`shared/tools.env`（相对本脚本位置）。

注意：**引用数随时间变化**，输出 TSV 的末列自动写入取数日期，便于事后判断时效。
"""

import argparse
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_ENV = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "tools.env"))
API = "https://api.semanticscholar.org/graph/v1/paper/batch"
DEFAULT_FIELDS = "title,year,venue,citationCount,influentialCitationCount,externalIds"
CHUNK = 100  # S2 单次 batch 上限 500，留余量


def load_key():
    key = os.environ.get("S2_API_KEY")
    if key:
        return key
    if os.path.exists(TOOLS_ENV):
        with open(TOOLS_ENV, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("export S2_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("错误：未找到 S2_API_KEY（既不在环境变量，也不在 shared/tools.env）")


def fetch(ids, fields, key, max_retry=5, base_delay=3.0):
    """单次 batch 调用；429 与 5xx 按指数退避重试。"""
    body = json.dumps({"ids": ids}).encode("utf-8")
    req = urllib.request.Request(
        "%s?fields=%s" % (API, fields),
        data=body,
        method="POST",
        headers={
            "x-api-key": key,
            "Content-Type": "application/json",
            "User-Agent": "AI4R-tools/1.0",
        },
    )
    for attempt in range(max_retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in (429,) or exc.code >= 500:
                if attempt == max_retry:
                    raise
                delay = base_delay * (2 ** attempt)
                print(
                    "    HTTP %d，%.0fs 后重试（%d/%d）" % (exc.code, delay, attempt + 1, max_retry),
                    file=sys.stderr,
                )
                time.sleep(delay)
            else:
                raise
    return []


def read_ids(args):
    ids = list(args.ids or [])
    if args.ids_file:
        with open(args.ids_file, encoding="utf-8") as fh:
            ids += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    if not ids and not sys.stdin.isatty():
        ids = [l.strip() for l in sys.stdin if l.strip() and not l.startswith("#")]
    if not ids:
        sys.exit("错误：没有输入 ID。用位置参数、--ids-file 或 stdin 提供。")
    return ids


def main():
    ap = argparse.ArgumentParser(description="Semantic Scholar 批量抓取（带 429 重试）")
    ap.add_argument("ids", nargs="*", help="论文 ID，如 arXiv:2307.15818 / DOI:10.xxx / PMID:123")
    ap.add_argument("--ids-file", help="从文件读 ID（每行一个，# 为注释）")
    ap.add_argument("--fields", default=DEFAULT_FIELDS, help="S2 字段列表，逗号分隔")
    ap.add_argument("--out", help="输出 TSV 路径（默认写到 stdout）")
    args = ap.parse_args()

    key = load_key()
    fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    ids = read_ids(args)
    today = datetime.date.today().isoformat()

    rows, failed = [], []
    for start in range(0, len(ids), CHUNK):
        chunk = ids[start:start + CHUNK]
        print("  批次 %d-%d / %d" % (start + 1, start + len(chunk), len(ids)), file=sys.stderr)
        try:
            data = fetch(chunk, args.fields, key)
        except Exception as exc:  # noqa: BLE001 —— 逐 ID 降级，不因一批失败丢掉全部
            print("    批次失败：%s" % exc, file=sys.stderr)
            failed.extend(chunk)
            continue
        # ⚠ 第七十九轮：校验返回形状，避免 zip 静默截断（长度不符 / 非 list 时整批记 failed，不丢行）
        if not isinstance(data, list) or len(data) != len(chunk):
            print("    批次返回异常（非 list 或长度不符），整批记 failed", file=sys.stderr)
            failed.extend(chunk)
            continue
        for want, got in zip(chunk, data):
            if got is None:
                failed.append(want)
                continue
            row = [want] + [got.get(f, "") for f in fields] + [today]
            rows.append(row)

    header = ["query_id"] + fields + ["fetched_on"]
    out_lines = ["\t".join(header)] + ["\t".join("" if v is None else str(v) for v in r) for r in rows]
    text = "\n".join(out_lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("写入 %s（%d 行）" % (args.out, len(rows)), file=sys.stderr)
    else:
        sys.stdout.write(text)

    if failed:
        print("未取到（%d 个）：%s" % (len(failed), ", ".join(failed)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
