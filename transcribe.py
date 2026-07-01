#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transcribe.py — Bóc băng file ghi âm cuộc họp thành văn bản (transcript).

Dùng Google Cloud Speech-to-Text (v2). Chạy được trên Mac và Windows.
KHÔNG cần tạo GCS bucket — script tự cắt audio thành từng khúc ngắn để xử lý.

CÁCH DÙNG:
    python transcribe.py <đường-dẫn-file-ghi-âm>
    python transcribe.py "hop-cong-ty.m4a"

KẾT QUẢ:
    Tạo file <tên-file>.txt trong thư mục transcripts/ — mỗi dòng có mốc thời gian.

YÊU CẦU:
    1) Đã cài ffmpeg  (xem docs/02-cai-dat.md)
    2) Có file "chìa khóa" Google Cloud (key.json) — xem docs/01-tao-google-cloud.md
       Đặt key.json ngay trong thư mục này, HOẶC set biến môi trường
       GOOGLE_APPLICATION_CREDENTIALS trỏ tới file key.
"""
import sys
import os
import json
import shutil
import subprocess
import tempfile
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNK_SEC = 50          # recognize() đồng bộ giới hạn ~60s/lần → cắt 50s cho an toàn
LANG = "vi-VN"          # tiếng Việt. Đổi nếu họp bằng ngôn ngữ khác, vd "en-US"


def die(msg):
    print("\n❌ " + msg + "\n")
    sys.exit(1)


def find_credentials():
    """Tìm file key Google. Ưu tiên biến môi trường, sau đó key.json trong repo."""
    env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if env:
        env = os.path.expanduser(env)
        if os.path.isfile(env):
            return env
        die("Biến GOOGLE_APPLICATION_CREDENTIALS đang trỏ tới file không tồn tại:\n"
            f"   {env}\n"
            "   → Sửa lại đường dẫn, hoặc bỏ biến này và đặt key.json trong thư mục meeting-agent/.")
    local = os.path.join(HERE, "key.json")
    if os.path.isfile(local):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local
        return local
    die("Chưa thấy file chìa khóa Google (key.json).\n"
        "   → Làm theo docs/01-tao-google-cloud.md để tải key.json,\n"
        "     rồi đặt nó ngay trong thư mục meeting-agent/.")


def project_id_from_key(key_path):
    try:
        with open(key_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        die("File key.json không đúng định dạng JSON. Tải lại từ Google Cloud Console.")
    except (OSError, IsADirectoryError, PermissionError):
        die("Không đọc được file key.json (thiếu quyền, hoặc đây là thư mục). Kiểm tra lại.")
    pid = data.get("project_id") or data.get("quota_project_id")
    if not pid:
        die("File key.json không có 'project_id'. Anh tải lại đúng file key service account.")
    return pid


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        die("Chưa cài ffmpeg (công cụ xử lý audio).\n"
            "   → Xem docs/02-cai-dat.md (Mac: brew install ffmpeg | Windows: winget install ffmpeg).")


def fmt(total_sec):
    m, s = divmod(int(total_sec), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main():
    if len(sys.argv) < 2:
        die("Thiếu đường dẫn file ghi âm.\n   Dùng: python transcribe.py <file-ghi-am>")

    audio_in = sys.argv[1]
    if os.path.isdir(audio_in):
        die(f"Đây là một thư mục, không phải file: {audio_in}\n   Hãy chọn đúng 1 file ghi âm.")
    if not os.path.isfile(audio_in):
        die(f"Không tìm thấy file: {audio_in}")

    check_ffmpeg()
    key_path = find_credentials()
    project_id = project_id_from_key(key_path)

    # Import sau khi đã báo lỗi ffmpeg/key (thư viện có thể nặng)
    try:
        from google.cloud import speech_v2
        from google.cloud.speech_v2.types import cloud_speech
    except ImportError:
        die("Chưa cài thư viện Google. Chạy: pip install -r requirements.txt\n"
            "   (hoặc chạy setup.sh / setup.bat trước).")

    recognizer = f"projects/{project_id}/locations/global/recognizers/_"

    base = os.path.splitext(os.path.basename(audio_in))[0]
    out_dir = os.path.join(HERE, "transcripts")
    os.makedirs(out_dir, exist_ok=True)
    out_txt = os.path.join(out_dir, f"{base}.txt")

    tmpdir = tempfile.mkdtemp(prefix="mtg_")
    print(f"🎧  Đang chuẩn bị audio: {os.path.basename(audio_in)}")
    lines = []
    failed = 0
    total = 0
    try:
        # Cắt audio thành từng khúc 16k mono để gọi STT
        try:
            seg = subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio_in,
                 "-f", "segment", "-segment_time", str(CHUNK_SEC),
                 "-ar", "16000", "-ac", "1",
                 os.path.join(tmpdir, "chunk_%04d.wav")],
                timeout=600,
            )
        except subprocess.TimeoutExpired:
            die("Xử lý audio quá lâu (timeout). File có thể quá lớn hoặc bị lỗi định dạng.")
        if seg.returncode != 0:
            die("ffmpeg không đọc được file này. File có bị hỏng / sai định dạng không?")

        chunks = sorted(glob.glob(os.path.join(tmpdir, "chunk_*.wav")))
        if not chunks:
            die("Không tạo được khúc audio nào (file rỗng?).")
        total = len(chunks)
        print(f"✂️   Chia thành {total} khúc (~{CHUNK_SEC}s/khúc). Bắt đầu bóc băng...")

        client = speech_v2.SpeechClient()
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[LANG],
            model="long",
            features=cloud_speech.RecognitionFeatures(enable_word_time_offsets=True),
        )

        for idx, ch in enumerate(chunks):
            base_off = idx * CHUNK_SEC
            with open(ch, "rb") as f:
                content = f.read()
            try:
                resp = client.recognize(
                    request=cloud_speech.RecognizeRequest(
                        recognizer=recognizer, config=config, content=content),
                    timeout=120)
            except Exception as e:
                msg = str(e)
                if "SERVICE_DISABLED" in msg or "has not been used" in msg:
                    die("API Speech-to-Text chưa được bật cho project này.\n"
                        "   → Xem docs/01-tao-google-cloud.md phần 'Bật API'.")
                if "PERMISSION_DENIED" in msg or "billing" in msg.lower():
                    die("Google từ chối quyền (thường do chưa bật Billing hoặc key sai quyền).\n"
                        "   → Kiểm tra lại docs/01-tao-google-cloud.md.")
                failed += 1
                print(f"  ⚠️  Khúc {idx+1} lỗi, bỏ qua: {msg[:120]}")
                continue
            for r in resp.results:
                if not r.alternatives:
                    continue
                alt = r.alternatives[0]
                start = base_off
                if alt.words:
                    start = base_off + alt.words[0].start_offset.total_seconds()
                text = alt.transcript.strip()
                if text:
                    lines.append(f"[{fmt(start)}] {text}")
            if (idx + 1) % 5 == 0 or idx + 1 == total:
                print(f"  ...{idx + 1}/{total} khúc")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    if not lines:
        die("Không nhận được chữ nào. File có tiếng nói rõ không? Ngôn ngữ có đúng vi-VN không?")

    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n✅  Xong! Transcript đã lưu tại:")
    print(f"    {out_txt}")
    if failed:
        print(f"\n⚠️  Lưu ý: {failed}/{total} khúc bị lỗi nên transcript có thể thiếu vài đoạn.")
        print("    Thử chạy lại; nếu vẫn lỗi, kiểm tra mạng hoặc hạn mức Google.")
    print("\n👉  Bước tiếp theo: mở file transcript, làm theo prompts/prompt-bien-ban.txt")
    print("    để dán vào ChatGPT / Claude / Gemini → nhận biên bản.")


if __name__ == "__main__":
    main()
