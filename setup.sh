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

# 2) ffmpeg — KHÔNG cần cài tay: đã đi kèm gói imageio-ffmpeg (cài ở bước dưới)
if command -v ffmpeg >/dev/null 2>&1; then
  echo "✔ ffmpeg đã có sẵn trong máy"
else
  echo "ℹ ffmpeg sẽ dùng bản đi kèm (tự cài qua pip) — không cần làm gì thêm"
fi

# 3) Tạo môi trường ảo + cài thư viện
echo "→ Tạo môi trường Python (.venv) và cài thư viện..."
python3 -m venv .venv
./.venv/bin/pip install --quiet --upgrade pip
./.venv/bin/pip install --quiet -r requirements.txt

echo ""
echo "✅ Cài đặt xong!"
echo "   • Tiếp theo: tạo file key.json theo docs/01-tao-google-cloud.md, đặt vào thư mục này."
echo "   • Để dùng: bấm đúp 'Chay tren Mac.command' và chọn trong menu."
