# Bước 4 (tùy chọn) — Đẩy công việc lên Google Sheet Gantt

Sau khi có biên bản, bạn có thể đẩy **bảng phân công công việc** lên một **Google Sheet dạng Gantt**
để theo dõi tiến độ (ai làm gì, khi nào, đến đâu). Đây là tính năng **tùy chọn** — bỏ qua cũng được.

```
   📄 Biên bản (bienban.md)
        │  bảng: Việc | Người | Deadline
        ▼
   📊 Google Sheet Gantt  →  thanh tiến độ tự vẽ theo ngày
```

---

## Chuẩn bị (làm 1 lần)

### 4.1. Lấy template Gantt (tiếng Việt)
Mở link này rồi bấm **"Tạo bản sao / Make a copy"** để có template trong Drive của bạn:

> https://docs.google.com/spreadsheets/d/19xZHxJYJsD17M-mlURx9QmEUvrD-Su_T3JGXjim_Ifw/copy

Template có 3 tab: **Biểu đồ Gantt · Danh sách CV · Hướng dẫn**. Thanh Gantt tự vẽ theo ngày,
việc **Bị chặn** tô đỏ, tự tính số ngày & % hoàn thành.

### 4.2. Bật thêm API cho service account
Dùng lại **chính service account** đã tạo ở [docs/01](01-tao-google-cloud.md) (cái dùng cho bóc băng).
Vào Google Cloud Console, bật thêm 2 API cho project đó:
- **Google Sheets API** → https://console.cloud.google.com/apis/library/sheets.googleapis.com → Enable
- **Google Drive API** → https://console.cloud.google.com/apis/library/drive.googleapis.com → Enable

### 4.3. Share sheet cho service account
1. Mở file Gantt vừa copy → bấm **Share**.
2. Dán **email service account** (trong file `key.json`, dòng `client_email`) → chọn **Editor**.

### 4.4. Lấy ID sheet
Từ URL: `docs.google.com/spreadsheets/d/`**`<ID_Ở_ĐÂY>`**`/edit` — copy đoạn ID.

---

## Cách dùng

```
python push_to_gantt.py bienban.md --sheet <ID_SHEET> --date 2026-07-02
```

- `--sheet`: ID Google Sheet Gantt (hoặc đặt sẵn biến môi trường `GANTT_SHEET_ID` rồi khỏi gõ).
- `--date`: ngày họp (dùng làm **ngày bắt đầu** cho các việc). Mặc định = hôm nay.

Kết quả: các việc trong biên bản được ghi vào tab **Biểu đồ Gantt**, thanh tiến độ tự vẽ.

---

## Lưu ý
- **Deadline dạng ngày** (vd `04/07/2026`) → vào cột **Kết thúc**, thanh Gantt tự hiện.
- **Deadline dạng chữ** (vd `cuối tháng`, `trước thứ Sáu`) → để trống ngày; bạn tự điền cột **Kết thúc**
  cho khớp, thanh sẽ hiện ngay.
- **Chế độ đồng bộ:** mỗi lần chạy sẽ **ghi đè** danh sách việc (xoá cũ, ghi mới) để chạy lại cùng
  một biên bản không bị trùng. Muốn giữ lịch sử từng buổi → **copy sheet** ra bản mới trước khi đẩy.
- **Nếu bạn dùng Claude Code / trợ lý AI:** chỉ cần nói *"đẩy công việc trong biên bản lên Gantt"*,
  trợ lý sẽ tự chạy lệnh này.

## Gặp lỗi
- **"Không mở được sheet"** → chưa share file cho email service account (bước 4.3), hoặc sai ID.
- **API lỗi / 403** → chưa bật Sheets API + Drive API (bước 4.2).
