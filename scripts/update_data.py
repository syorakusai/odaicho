#!/usr/bin/env python3
"""
妖怪物語データ更新スクリプト

Googleスプレッドシート（「リンクを知っている全員が閲覧者」設定必須）を
CSVとしてエクスポートし、story.html が読み込む data/yokai.json を作り直す。

GitHub Actions から毎日自動実行される想定。手動実行も可能:
    python3 scripts/update_data.py
"""
import csv
import io
import json
import sys
import urllib.request

SPREADSHEET_ID = "1wZdtdfVxkcjknxeXhncrokapdMmck5rfm7NHHDOQiuY"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
OUTPUT_PATH = "data/yokai.json"

# 列インデックス（0始まり）: A=0, B=1, ... F=5, R=17
COL_NO = 0
COL_NAME = 1
COL_F = 5
COL_POSTDATE = 7
COL_R = 17

MARKER = "【特質】"


def fetch_csv_text() -> str:
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    return raw.decode("utf-8")


def build_records(csv_text: str) -> list:
    reader = csv.reader(io.StringIO(csv_text))
    header = next(reader, None)
    records = []
    for row in reader:
        if not row or not row[0].strip().isdigit():
            continue
        name = row[COL_NAME].strip() if len(row) > COL_NAME else ""
        if not name:
            # 未記入の下書き行はスキップ
            continue
        no = int(row[COL_NO].strip())
        f_col = row[COL_F] if len(row) > COL_F else ""
        r_col = row[COL_R] if len(row) > COL_R else ""
        post_date = row[COL_POSTDATE].strip() if len(row) > COL_POSTDATE else ""

        idx = r_col.find(MARKER)
        if idx == -1:
            before, after = r_col, ""
        else:
            before, after = r_col[:idx], r_col[idx:]

        records.append({
            "no": no,
            "name": name,
            "f": f_col,
            "rBefore": before,
            "rAfter": after,
            "postDate": post_date,
        })
    records.sort(key=lambda d: d["no"])
    return records


def main():
    try:
        csv_text = fetch_csv_text()
    except Exception as e:
        print(f"ERROR: スプレッドシートの取得に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    records = build_records(csv_text)
    if not records:
        print("ERROR: 取得したデータが0件でした。処理を中断します。", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)

    print(f"OK: {len(records)}件を {OUTPUT_PATH} に書き出しました。")


if __name__ == "__main__":
    main()
