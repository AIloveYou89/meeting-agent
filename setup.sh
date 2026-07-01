#!/bin/bash
# setup.sh — Cài đặt 1 lần cho macOS / Linux.
# Chạy:  bash setup.sh
set -e
cd "$(dirname "$0")"

echo "=================================================="
echo "  MEETING-AGENT — Cài đặt"
echo "=================================================="

# 1) Kiểm tra Python
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Chưa có Python 3. Cài tại: https://www.python.org/downloads/"
  exit 1
fi
echo "✔ Python: $(python3 --version)"

# 2) Kiểm tra ffmpeg
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "⚠ Chưa có ffmpeg. Cài bằng:"
  echo "    macOS:  brew install ffmpeg"
  echo "    Linux:  sudo apt install ffmpeg"
  echo "  (Cài xong chạy lại setup.sh)"
else
  echo "✔ ffmpeg đã có"
fi

# 3) Tạo môi trường ảo + cài thư viện
echo "→ Tạo môi trường Python (.venv) và cài thư viện..."
python3 -m venv .venv
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt

echo ""
echo "✅ Xong! Các bước tiếp theo:"
echo "   1) Tạo file key.json theo docs/01-tao-google-cloud.md, đặt vào thư mục này."
echo "   2) Bóc băng:   ./.venv/bin/python transcribe.py \"file-ghi-am.m4a\""
echo "   3) Dựng Word:  ./.venv/bin/python make_bienban.py bienban.md"
