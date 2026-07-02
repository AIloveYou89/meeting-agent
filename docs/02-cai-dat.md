# Bước 2 — Cài đặt (làm 1 lần, ~5 phút)

Chỉ cần **cài Python 1 lần**, rồi **bấm đúp 1 file** là xong.
Bạn **KHÔNG** phải cài ffmpeg hay gõ lệnh gì cả — chương trình tự lo.

---

## 🍎 Trên macOS

**1. Cài Python** (nếu máy chưa có)
- Vào **https://www.python.org/downloads/** → bấm nút vàng **"Download Python"**.
- Mở file `.pkg` vừa tải → bấm **Continue → Continue → Install** (next-next là xong).

**2. Bấm đúp để chạy**
- Mở thư mục `meeting-agent` → **bấm đúp vào file `Chay tren Mac.command`**.
- Lần đầu nó sẽ **tự cài đặt** (mất 1-2 phút), sau đó hiện **menu**.

> ⚠️ **Nếu macOS báo "không mở được vì từ nhà phát triển không xác định":**
> **bấm chuột phải** vào `Chay tren Mac.command` → chọn **Open** → **Open** lần nữa.
> (Chỉ cần làm 1 lần đầu, từ sau bấm đúp là chạy.)

---

## 🪟 Trên Windows

**1. Cài Python** (nếu máy chưa có)
- Vào **https://www.python.org/downloads/** → tải **Python**.
- Khi cài **nhớ tick ô "Add Python to PATH"** ở màn hình đầu → rồi bấm **Install Now**.

**2. Bấm đúp để chạy**
- Mở thư mục `meeting-agent` → **nhấp đôi vào file `Chay tren Windows.bat`**.
- Lần đầu nó **tự cài đặt** (1-2 phút), rồi hiện **menu**.

> 💡 Mẹo: bạn có thể **kéo thẳng 1 file ghi âm** thả lên icon `Chay tren Windows.bat` —
> nó sẽ bóc băng file đó luôn, khỏi cần vào menu.

---

## Sau khi cài xong, menu trông như này:
```
   1) Bóc băng file ghi âm   →  chữ (transcript)
   2) Tạo biên bản Word từ file bienban.md
   3) (nâng cao) Đẩy công việc lên Google Sheet Gantt
   4) Cài đặt lại / cập nhật
   0) Thoát
```
Chọn **1**, rồi **kéo file ghi âm thả vào cửa sổ** → Enter là chạy.

---

## Còn thiếu 1 thứ: "chìa khóa" Google
Để bóc băng được, bạn cần file **`key.json`** đặt trong thư mục `meeting-agent`.
Nếu chưa có → làm theo **[docs/01-tao-google-cloud.md](01-tao-google-cloud.md)** (có ảnh từng bước).

✅ Xong bước 2. Sang **[docs/03-su-dung.md](03-su-dung.md)** để tạo biên bản.

---

### Gặp lỗi thường gặp
- **Windows báo "python is not recognized":** bạn quên tick **"Add Python to PATH"** — gỡ Python ra, cài lại và nhớ tick.
- **macOS chặn không cho mở file `.command`:** bấm chuột phải → **Open** (xem lưu ý ở trên).
- **Bấm đúp mà không thấy gì:** mở lại thư mục, thử chuột phải → Open. Nếu vẫn lỗi, xem đã cài Python chưa.
