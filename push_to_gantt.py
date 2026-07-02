#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
push_to_gantt.py — Đẩy bảng phân công trong biên bản họp lên Google Sheet Gantt.

Đọc file biên bản (bienban.md) → lấy bảng "phân công công việc"
(Việc | Người phụ trách | Thời hạn) → ghi vào 1 Google Sheet dạng Gantt.

CÁCH DÙNG:
    python push_to_gantt.py bienban.md
    python push_to_gantt.py bienban.md --sheet <ID_SHEET> --date 2026-07-02

CHUẨN BỊ (làm 1 lần) — xem docs/04-day-task-len-gantt.md:
    1) Copy template Gantt về Drive của bạn.
    2) Bật Google Sheets API + Drive API cho service account (cùng cái dùng cho Speech).
    3) Share sheet đó cho email service account (Editor).
    4) Đặt ID sheet vào biến môi trường GANTT_SHEET_ID (hoặc dùng --sheet).

GHI CHÚ:
    - Chế độ "đồng bộ": mỗi lần chạy sẽ ghi ĐÈ danh sách việc (xoá việc cũ, ghi việc mới)
      để chạy lại cùng biên bản không bị trùng. Muốn giữ lịch sử → copy sheet trước.
    - Deadline nếu là ngày cụ thể (04/07/2026) sẽ vào cột "Kết thúc" và thanh Gantt tự vẽ.
      Deadline dạng chữ ("cuối tháng") thì để trống ngày, bạn tự điền sau.
"""
import sys
import os
import re
import argparse
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
GANTT_TAB = "Biểu đồ Gantt"     # tên tab trong template (tiếng Việt)
FIRST_ROW = 8                    # dòng bắt đầu ghi việc trong template
LAST_ROW = 22                    # dòng cuối vùng việc (template có 15 dòng: 8..22)


def die(msg):
    print("\n❌ " + msg + "\n")
    sys.exit(1)


# ---------------- Parse bảng phân công từ markdown ----------------
def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def parse_tasks(md_text):
    """Tìm bảng có cột 'Người phụ trách' → trả về list (viec, nguoi, deadline)."""
    lines = md_text.replace("\r\n", "\n").split("\n")
    tasks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "|" in line and re.search(r"người|phụ trách|owner", line, re.I) \
                and re.search(r"việc|task|công việc", line, re.I):
            header = [h.lower() for h in _split_row(line)]
            # xác định cột
            def find(*keys):
                for idx, h in enumerate(header):
                    if any(k in h for k in keys):
                        return idx
                return None
            ci_task = find("việc", "task", "công việc")
            ci_owner = find("người", "phụ trách", "owner")
            ci_dl = find("hạn", "deadline", "thời hạn", "kết thúc")
            i += 1
            if i < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i]):
                i += 1  # bỏ dòng ngăn cách ---
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                cells = _split_row(lines[i])
                def get(ci):
                    return cells[ci].strip() if ci is not None and ci < len(cells) else ""
                task = get(ci_task)
                if task:
                    tasks.append((task, get(ci_owner), get(ci_dl)))
                i += 1
            break
        i += 1
    return tasks


# ---------------- Parse ngày từ chuỗi deadline ----------------
def parse_deadline(text):
    """Trả về 'YYYY-MM-DD' nếu tìm được ngày trong chuỗi, ngược lại None."""
    if not text:
        return None
    m = re.search(r"(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?", text)
    if not m:
        return None
    d, mo = int(m.group(1)), int(m.group(2))
    y = m.group(3)
    y = int(y) if y else date.today().year
    if y < 100:
        y += 2000
    try:
        return datetime(y, mo, d).strftime("%Y-%m-%d")
    except ValueError:
        return None


def find_credentials():
    env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if env and os.path.isfile(os.path.expanduser(env)):
        return os.path.expanduser(env)
    local = os.path.join(HERE, "key.json")
    if os.path.isfile(local):
        return local
    die("Chưa thấy file chìa khóa Google (key.json). Xem docs/01 để tạo,\n"
        "   và docs/04 để bật Sheets/Drive API + share sheet cho service account.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bienban", help="đường dẫn file biên bản .md")
    ap.add_argument("--sheet", default=os.environ.get("GANTT_SHEET_ID"),
                    help="ID Google Sheet Gantt (hoặc đặt GANTT_SHEET_ID)")
    ap.add_argument("--date", default=date.today().strftime("%Y-%m-%d"),
                    help="ngày họp (YYYY-MM-DD) dùng làm ngày bắt đầu task; mặc định hôm nay")
    args = ap.parse_args()

    if not os.path.isfile(args.bienban):
        die(f"Không tìm thấy file biên bản: {args.bienban}")
    if not args.sheet:
        die("Chưa có ID sheet. Dùng --sheet <ID> hoặc đặt biến GANTT_SHEET_ID.\n"
            "   (Lấy ID từ URL: docs.google.com/spreadsheets/d/<ID>/edit)")

    with open(args.bienban, "r", encoding="utf-8-sig") as f:
        md = f.read()
    tasks = parse_tasks(md)
    if not tasks:
        die("Không tìm thấy bảng phân công trong biên bản.\n"
            "   (Cần 1 bảng có cột 'Việc' và 'Người phụ trách'.)")

    try:
        import gspread
    except ImportError:
        die("Chưa cài gspread. Chạy: pip install -r requirements.txt")

    cred = find_credentials()
    gc = gspread.service_account(filename=cred)
    try:
        sh = gc.open_by_key(args.sheet)
    except Exception as e:
        die(f"Không mở được sheet (đã share cho service account chưa?).\n   Chi tiết: {str(e)[:150]}")
    try:
        ws = sh.worksheet(GANTT_TAB)
    except Exception:
        ws = sh.sheet1  # fallback nếu tab tên khác

    # Xoá vùng việc cũ (chế độ đồng bộ) — chừa cột F (Số ngày = công thức)
    ws.batch_clear([f"A{FIRST_ROW}:E{LAST_ROW}", f"G{FIRST_ROW}:H{LAST_ROW}"])

    n = 0
    ae_rows, gh_rows = [], []
    for idx, (task, owner, deadline) in enumerate(tasks):
        row = FIRST_ROW + idx
        if row > LAST_ROW:
            print(f"⚠️  Template chỉ chứa {LAST_ROW-FIRST_ROW+1} việc — {len(tasks)-(LAST_ROW-FIRST_ROW+1)} việc dư bị bỏ. "
                  "Mở rộng template nếu cần (xem tab Hướng dẫn).")
            break
        end = parse_deadline(deadline)
        start = args.date if end else ""     # có ngày kết thúc mới đặt ngày bắt đầu
        ae_rows.append([idx + 1, task, owner, start, end or ""])
        gh_rows.append([0, "Chưa bắt đầu"])
        n += 1

    ws.update(range_name=f"A{FIRST_ROW}:E{FIRST_ROW+n-1}", values=ae_rows, value_input_option="USER_ENTERED")
    ws.update(range_name=f"G{FIRST_ROW}:H{FIRST_ROW+n-1}", values=gh_rows, value_input_option="USER_ENTERED")

    print(f"\n✅  Đã đẩy {n} việc lên Gantt.")
    no_date = sum(1 for t in tasks[:n] if not parse_deadline(t[2]))
    if no_date:
        print(f"   ({no_date} việc có deadline dạng chữ → chưa có ngày, bạn tự điền cột Kết thúc để thanh Gantt hiện.)")
    print(f"   Mở sheet: https://docs.google.com/spreadsheets/d/{args.sheet}")


if __name__ == "__main__":
    main()
