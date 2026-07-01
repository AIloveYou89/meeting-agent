# Bước 3 — Tạo biên bản từ file ghi âm

Sau khi đã xong bước 1 (có `key.json`) và bước 2 (đã cài đặt), mỗi lần muốn tạo biên bản chỉ có **3 việc**.

> Ghi chú: các lệnh dưới dùng `python`. Nếu bạn chạy `setup.sh`/`setup.bat`, có thể thay bằng
> - macOS/Linux: `./.venv/bin/python`
> - Windows: `.venv\Scripts\python`

---

## ① Bóc băng: file ghi âm → văn bản

Đặt file ghi âm (`.m4a`, `.mp3`, `.wav`...) vào thư mục `meeting-agent`, rồi chạy:

```
python transcribe.py "ten-file-ghi-am.m4a"
```

- Máy sẽ chia nhỏ audio và gửi lên Google để nhận dạng.
- Họp càng dài chạy càng lâu (1 tiếng họp mất khoảng vài phút).
- Xong sẽ có file **`transcripts/ten-file-ghi-am.txt`** — bản chữ có mốc thời gian.

---

## ② Nhờ AI viết biên bản

Bạn dùng **bất kỳ AI nào đang có sẵn** (ChatGPT, Claude, Gemini, Copilot... — kể cả bản miễn phí):

1. Mở file **`prompts/prompt-bien-ban.txt`**, copy toàn bộ nội dung.
2. Mở file transcript vừa tạo ở bước ①, copy toàn bộ.
3. Vào AI, **dán prompt trước, rồi dán transcript vào ngay dưới dòng "DÁN TRANSCRIPT VÀO ĐÂY"**, gửi.
4. AI trả về biên bản dạng Markdown. **Copy toàn bộ** phần đó.
5. Tạo file mới tên **`bienban.md`** trong thư mục `meeting-agent`, dán vào, lưu lại.

> 💡 Nếu AI trả lời kèm lời chào/giải thích, chỉ cần lấy phần bắt đầu từ `# BIÊN BẢN CUỘC HỌP`.

---

## ③ Xuất ra file Word

```
python make_bienban.py bienban.md
```

Xong! Bạn có file **`bienban.docx`** — mở bằng Word để chỉnh sửa, in, ký.

---

## Thử nhanh với ví dụ mẫu (không cần file ghi âm)
Muốn xem thành phẩm ngay, dùng luôn file mẫu có sẵn:
```
python make_bienban.py examples/bienban-mau.md
```
→ ra `examples/bienban-mau.docx`. Đây là biên bản mẫu từ một cuộc họp giả định.

---

## Mẹo để bản ghi âm ra chữ chính xác hơn
- Đặt điện thoại/máy ghi âm **gần người nói**, phòng càng ít ồn càng tốt.
- Mọi người nói **rõ ràng, không chồng lời** nhau.
- Họp online: bật ghi âm của Zoom/Google Meet rồi tải file về dùng.
