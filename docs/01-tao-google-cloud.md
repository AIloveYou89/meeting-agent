# Bước 1 — Tạo "chìa khóa" Google Cloud (làm 1 lần duy nhất)

> Để máy tính bóc được file ghi âm thành chữ, ta mượn dịch vụ **Speech-to-Text của Google**.
> Bạn cần tạo một tài khoản Google Cloud và tải về **1 file chìa khóa** (`key.json`).
> Nghe hơi kỹ thuật nhưng cứ làm tuần tự bên dưới là xong, khoảng **10–15 phút**.

> 💡 **Chi phí:** Google cho **60 phút bóc băng MIỄN PHÍ mỗi tháng**. Quá 60 phút thì tính
> khoảng **~400đ/phút** (họp 1 tiếng ≈ 24.000đ). Google **không tự trừ tiền** nếu bạn chưa
> chủ động bật thẻ; và bạn có thể đặt hạn mức để không lo phát sinh.

---

## 1.1. Đăng nhập Google Cloud Console
1. Vào **https://console.cloud.google.com** bằng tài khoản Gmail của bạn.
2. Lần đầu vào, Google hỏi đồng ý điều khoản → tick đồng ý → **Agree and Continue**.

## 1.2. Tạo một "Project" (dự án)
1. Ở thanh trên cùng, bấm vào ô chọn project (cạnh chữ "Google Cloud").
2. Bấm **New Project** (Dự án mới).
3. Đặt tên, ví dụ `bien-ban-hop` → bấm **Create**.
4. Chờ vài giây, rồi bấm lại ô chọn project và **chọn đúng project vừa tạo**.

## 1.3. Bật dịch vụ Speech-to-Text
1. Vào link: **https://console.cloud.google.com/apis/library/speech.googleapis.com**
2. Kiểm tra góc trên đang đúng project của bạn.
3. Bấm nút **Enable** (Bật). Chờ đến khi hiện "API enabled".

## 1.4. Bật thanh toán (Billing) — bắt buộc, kể cả khi dùng bản miễn phí
> Google yêu cầu có thẻ để "xác minh", nhưng vẫn cho 60 phút free/tháng. Không dùng quá thì không mất tiền.
1. Vào **https://console.cloud.google.com/billing**
2. Bấm **Link a billing account** hoặc **Create account** → làm theo hướng dẫn, thêm thẻ Visa/Mastercard.
3. Gắn billing account đó vào project vừa tạo.

## 1.5. Tạo "Service Account" và tải file chìa khóa (`key.json`)
Đây là bước tạo ra file chìa khóa cho phần mềm dùng.

1. Vào **https://console.cloud.google.com/iam-admin/serviceaccounts**
2. Bấm **Create Service Account**.
   - **Name:** `meeting-agent` → **Create and Continue**.
   - **Role (cấp quyền):** chọn `Cloud Speech Client` (gõ "speech" để tìm).
     Nếu không thấy, chọn tạm `Project → Editor` cũng được.
   - Bấm **Continue** → **Done**.
3. Trong danh sách, bấm vào service account `meeting-agent` vừa tạo.
4. Qua tab **Keys** → **Add Key** → **Create new key** → chọn **JSON** → **Create**.
5. Trình duyệt sẽ **tải về 1 file `.json`**. Đây chính là **chìa khóa** của bạn.

## 1.6. Đặt file chìa khóa vào đúng chỗ
1. Đổi tên file vừa tải thành **`key.json`**.
2. **Copy vào thư mục `meeting-agent`** (ngay cạnh file `transcribe.py`).

✅ **Xong bước 1.** File `key.json` đã sẵn sàng. Sang **docs/02-cai-dat.md**.

---

## ⚠️ Lưu ý bảo mật (rất quan trọng)
- File `key.json` giống như **chìa khóa nhà** — ai có nó cũng dùng được tài khoản Google Cloud của bạn.
- **KHÔNG** gửi file này cho ai, **KHÔNG** đưa lên GitHub / Facebook / email.
- Phần mềm đã tự động chặn (`.gitignore`) để bạn không lỡ tay đẩy `key.json` lên mạng.
- Nếu lỡ để lộ: vào lại mục **Service Accounts → Keys**, xóa key cũ và tạo key mới.
