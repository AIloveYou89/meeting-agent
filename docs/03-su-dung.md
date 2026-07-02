# Bước 3 — Tạo biên bản từ file ghi âm

Sau khi xong bước 1 (có `key.json`) và bước 2 (đã cài đặt), mỗi lần tạo biên bản chỉ có **3 việc**.

> Mở chương trình: **bấm đúp** `Chay tren Mac.command` (Mac) hoặc `Chay tren Windows.bat` (Windows)
> → hiện menu. Chọn số tương ứng bên dưới.

---

## ① Bóc băng: file ghi âm → văn bản  *(menu → 1)*

1. Đặt file ghi âm (`.m4a`, `.mp3`, `.wav`...) ở đâu cũng được.
2. Trong menu, gõ **1** rồi Enter.
3. **Kéo file ghi âm thả vào cửa sổ** → Enter.

- Máy sẽ chia nhỏ audio và gửi lên Google để nhận dạng.
- Họp càng dài chạy càng lâu (1 tiếng họp mất khoảng vài phút).
- Xong sẽ có file **`transcripts/ten-file.txt`** — bản chữ có mốc thời gian.

> 🪟 Trên Windows còn nhanh hơn: **kéo thẳng file ghi âm thả lên icon** `Chay tren Windows.bat`
> là nó bóc băng luôn, khỏi vào menu.

---

## ② Nhờ AI viết biên bản

Dùng **bất kỳ AI nào bạn đang có** (ChatGPT, Claude, Gemini, Copilot... — kể cả bản miễn phí):

1. Mở file **`prompts/prompt-bien-ban.txt`**, copy toàn bộ nội dung.
2. Mở file transcript vừa tạo ở bước ①, copy toàn bộ.
3. Vào AI, **dán prompt trước, rồi dán transcript vào ngay dưới dòng "DÁN TRANSCRIPT VÀO ĐÂY"**, gửi.
4. AI trả về biên bản dạng Markdown. **Copy toàn bộ** phần đó.
5. Tạo file mới tên **`bienban.md`** trong thư mục `meeting-agent`, dán vào, lưu lại.

> 💡 Nếu AI trả lời kèm lời chào/giải thích, chỉ cần lấy phần bắt đầu từ `# BIÊN BẢN CUỘC HỌP`.

---

## ③ Xuất ra file Word  *(menu → 2)*

Trong menu gõ **2** → Enter (để trống sẽ tự dùng `bienban.md`).
Xong! Bạn có file **`bienban.docx`** — mở bằng Word để chỉnh sửa, in, ký.

---

> ⚡ **Nếu bạn dùng trợ lý AI chạy được lệnh (Claude Code, Codex...):** bỏ qua cả copy-paste lẫn menu.
> Chỉ cần nói *"transcribe file ghi âm này rồi viết biên bản"* — trợ lý tự chạy hết.

---

## Cách khác: gõ lệnh (cho ai quen dùng terminal)
```
# Mac:      ./.venv/bin/python transcribe.py "ten-file.m4a"
#           ./.venv/bin/python make_bienban.py bienban.md
# Windows:  .venv\Scripts\python transcribe.py "ten-file.m4a"
#           .venv\Scripts\python make_bienban.py bienban.md
```

## Thử nhanh với ví dụ mẫu (không cần file ghi âm)
Trong menu gõ **2**, rồi kéo file `examples/bienban-mau.md` vào → ra `examples/bienban-mau.docx`.

---

## Mẹo để bản ghi âm ra chữ chính xác hơn
- Đặt điện thoại/máy ghi âm **gần người nói**, phòng càng ít ồn càng tốt.
- Mọi người nói **rõ ràng, không chồng lời** nhau.
- Họp online: bật ghi âm của Zoom/Google Meet rồi tải file về dùng.
