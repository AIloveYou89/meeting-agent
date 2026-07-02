# AGENTS.md — Hướng dẫn cho AI agent

> File này dành cho **AI coding agent** (Claude Code, Cursor, Codex, Gemini CLI...).
> Khi người dùng mở repo bằng agent, hãy đọc file này và **tự chạy trọn quy trình** —
> KHÔNG bắt người dùng copy-paste sang AI khác (vì **bạn chính là** AI làm việc đó).

## Repo này làm gì
`meeting-agent`: file ghi âm cuộc họp → transcript (Google Speech-to-Text) → **biên bản Word**
có tóm tắt, quyết định và **bảng phân công ai làm việc gì**.

---

## Khi người dùng đưa 1 file ghi âm (hoặc nói "làm biên bản cuộc họp"), làm tuần tự:

### B0 — Kiểm tra điều kiện
1. **Môi trường Python:** nếu chưa có thư mục `.venv` → cài trước:
   - macOS/Linux: `bash setup.sh`
   - Windows: `setup.bat`
2. **Chìa khóa Google (`key.json`):** phải có `key.json` ở thư mục gốc
   (hoặc biến môi trường `GOOGLE_APPLICATION_CREDENTIALS`).
   - **Chưa có → DỪNG lại**, hướng dẫn người dùng làm theo `docs/01-tao-google-cloud.md`.
     Đây là việc **DUY NHẤT** người dùng phải tự làm (1 lần). **Tuyệt đối không tự tạo/bịa** file này.

### B1 — Bóc băng (audio → transcript)
- macOS/Linux: `./.venv/bin/python transcribe.py "<đường-dẫn-file-ghi-âm>"`
- Windows: `.venv\Scripts\python transcribe.py "<đường-dẫn-file-ghi-âm>"`
- Kết quả: `transcripts/<tên-file>.txt` (có mốc thời gian).

### B2 — Viết biên bản (CHÍNH BẠN viết, lưu ra `bienban.md`)
1. Đọc `prompts/prompt-bien-ban.txt` — đó là **bản yêu cầu định dạng** biên bản.
2. Đọc transcript vừa tạo ở B1.
3. **Tự viết** biên bản đúng theo format đó, **lưu vào `bienban.md`** (UTF-8).
   - Giữ nguyên cấu trúc, đặc biệt là bảng `| Việc cần làm | Người phụ trách | Thời hạn |`
     (bảng này là đầu vào cho bước Gantt).
   - Không bịa thông tin không có trong transcript; nội dung không rõ thì ghi "(chưa rõ)".

### B3 — Xuất Word
- macOS/Linux: `./.venv/bin/python make_bienban.py bienban.md`
- Windows: `.venv\Scripts\python make_bienban.py bienban.md`
- Kết quả: `bienban.docx` → báo người dùng mở bằng Word.

### B4 (tùy chọn) — Đẩy công việc lên Google Sheet Gantt
Chỉ làm khi người dùng yêu cầu ("đẩy lên Gantt / timeline").
- Điều kiện: đã bật Sheets API + Drive API và **share sheet cho email service account** (`docs/04-day-task-len-gantt.md`).
- `./.venv/bin/python push_to_gantt.py bienban.md --sheet <ID_SHEET>`
  (hoặc đặt sẵn biến `GANTT_SHEET_ID`).

---

## Nguyên tắc BẮT BUỘC
- **KHÔNG** in/hiển thị nội dung `key.json` ra chat; **KHÔNG** commit nó.
- **KHÔNG** commit file ghi âm, thư mục `transcripts/`, hay `*.docx` (đã có `.gitignore` chặn — đừng gỡ).
- Ngôn ngữ mặc định **`vi-VN`**. Họp bằng ngôn ngữ khác → sửa hằng `LANG` trong `transcribe.py`.
- Một bước lỗi → **đọc thông báo lỗi, sửa hoặc giải thích cho người dùng**, không bỏ qua âm thầm.
- Sau khi xong, tóm tắt ngắn cho người dùng: đã tạo file gì, ở đâu, bước tiếp theo là gì.

## Người dùng KHÔNG có agent thì sao?
Họ dùng bản bấm đúp: `Chay tren Mac.command` / `Chay tren Windows.bat` → menu. Xem `README.md`.
