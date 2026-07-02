#!/bin/bash
# Chay tren Mac.command — Bấm đúp (double-click) để mở meeting-agent.
# Lần đầu sẽ tự cài đặt. Sau đó hiện menu: bóc băng / tạo Word / Gantt.
cd "$(dirname "$0")"
PY="./.venv/bin/python"

# --- Lần đầu: tự cài đặt môi trường ---
if [ ! -x "$PY" ]; then
  echo "Lần đầu chạy — đang cài đặt (mất 1-2 phút)..."
  if ! bash setup.sh; then
    echo ""
    echo "❌ Cài đặt chưa xong. Xem docs/02-cai-dat.md để cài Python trước."
    read -r -p "Nhấn Enter để đóng..." _
    exit 1
  fi
fi

# Bỏ dấu nháy / bỏ ký tự thoát khoảng trắng khi kéo file từ Finder vào Terminal
clean_path() {
  local p="$1"
  p="${p%\"}"; p="${p#\"}"          # bỏ nháy kép
  p="${p%\'}"; p="${p#\'}"          # bỏ nháy đơn
  p="$(printf '%s' "$p" | sed 's/\\ / /g')"   # bỏ dấu \ trước khoảng trắng
  # bỏ khoảng trắng thừa đầu/cuối
  p="$(printf '%s' "$p" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
  printf '%s' "$p"
}

while true; do
  clear
  echo "=================================================="
  echo "   🎙️  MEETING-AGENT"
  echo "=================================================="
  echo "   1) Bóc băng file ghi âm   →  chữ (transcript)"
  echo "   2) Tạo biên bản Word từ file bienban.md"
  echo "   3) (nâng cao) Đẩy công việc lên Google Sheet Gantt"
  echo "   4) Cài đặt lại / cập nhật thư viện"
  echo "   0) Thoát"
  echo "--------------------------------------------------"
  read -r -p "   Chọn (1 / 2 / 3 / 4 / 0): " choice
  echo ""
  case "$choice" in
    1)
      echo "👉 KÉO file ghi âm từ Finder, THẢ vào cửa sổ này, rồi nhấn Enter:"
      read -r -e raw
      f="$(clean_path "$raw")"
      if [ -z "$f" ]; then echo "Bạn chưa chọn file."; else "$PY" transcribe.py "$f"; fi
      read -r -p "— Nhấn Enter để về menu —" _
      ;;
    2)
      echo "👉 KÉO file biên bản (.md) vào đây rồi Enter (để trống = dùng bienban.md):"
      read -r -e raw
      f="$(clean_path "$raw")"
      [ -z "$f" ] && f="bienban.md"
      "$PY" make_bienban.py "$f"
      read -r -p "— Nhấn Enter để về menu —" _
      ;;
    3)
      echo "👉 KÉO file biên bản (.md) vào đây rồi Enter (để trống = dùng bienban.md):"
      read -r -e raw
      f="$(clean_path "$raw")"
      [ -z "$f" ] && f="bienban.md"
      echo "Nhập ID Google Sheet Gantt (bỏ trống nếu đã đặt biến GANTT_SHEET_ID):"
      read -r sid
      if [ -n "$sid" ]; then
        "$PY" push_to_gantt.py "$f" --sheet "$sid"
      else
        "$PY" push_to_gantt.py "$f"
      fi
      read -r -p "— Nhấn Enter để về menu —" _
      ;;
    4)
      bash setup.sh
      read -r -p "— Nhấn Enter để về menu —" _
      ;;
    0)
      exit 0
      ;;
    *)
      echo "Chọn không hợp lệ. Gõ 1, 2, 3, 4 hoặc 0."
      read -r -p "— Nhấn Enter —" _
      ;;
  esac
done
