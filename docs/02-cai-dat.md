# Bước 2 — Cài đặt phần mềm trên máy (làm 1 lần)

Cần 2 thứ: **Python** (để chạy chương trình) và **ffmpeg** (để xử lý âm thanh).

---

## Trên macOS

1. **Cài Homebrew** (nếu chưa có) — mở ứng dụng **Terminal**, dán dòng này rồi Enter:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. **Cài Python và ffmpeg:**
   ```
   brew install python ffmpeg
   ```
3. **Chạy cài đặt tự động** — trong Terminal, đi tới thư mục meeting-agent rồi chạy:
   ```
   cd ~/meeting-agent
   bash setup.sh
   ```

---

## Trên Windows

1. **Cài Python:** tải tại **https://www.python.org/downloads/**
   → khi cài **nhớ tick ô "Add Python to PATH"** rồi bấm Install.
2. **Cài ffmpeg:** mở **Command Prompt** (gõ `cmd` ở menu Start), chạy:
   ```
   winget install Gyan.FFmpeg
   ```
   (Cài xong **đóng và mở lại** cửa sổ Command Prompt.)
3. **Chạy cài đặt tự động:** mở thư mục `meeting-agent`, **nhấp đôi vào file `setup.bat`**
   (hoặc trong Command Prompt: `cd` vào thư mục rồi gõ `setup.bat`).

---

## Kiểm tra đã cài xong chưa
Gõ 2 lệnh sau, nếu ra số phiên bản là được:
```
python --version
ffmpeg -version
```

✅ Xong bước 2. Sang **docs/03-su-dung.md** để bắt đầu tạo biên bản.

---

### Gặp lỗi thường gặp
- **"python: command not found" (Windows):** bạn quên tick "Add Python to PATH" — gỡ Python ra cài lại và nhớ tick.
- **"ffmpeg: command not found":** chưa cài ffmpeg, hoặc chưa mở lại cửa sổ dòng lệnh sau khi cài.
- **macOS chặn Terminal:** vào System Settings → Privacy & Security, cho phép chạy.
