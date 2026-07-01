#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_bienban.py — Biến file biên bản dạng Markdown (do AI viết) thành file Word (.docx).

KHÔNG cần cài thêm thư viện nào — chỉ dùng thư viện chuẩn của Python.

CÁCH DÙNG:
    python make_bienban.py <file-bien-ban.md>
    python make_bienban.py bienban.md

KẾT QUẢ:
    Tạo file .docx cùng tên, cùng thư mục với file .md.

Markdown hỗ trợ:
    # / ## / ###      → tiêu đề các cấp
    **chữ đậm**       → in đậm
    - hoặc *          → gạch đầu dòng
    1. 2. 3.          → danh sách đánh số
    | a | b |         → bảng (dòng --- ngăn cách header sẽ tự bỏ)
    ---               → đường kẻ ngang
"""
import sys
import os
import re
import zipfile
from xml.sax.saxutils import escape


def _build_xml_invalid():
    """Regex bắt các ký tự KHÔNG hợp lệ trong XML 1.0 (nếu lọt vào Word sẽ báo file hỏng).
    Dựng từ code point để tránh mọi ký tự đặc biệt trong mã nguồn."""
    valid = [(0x9, 0x9), (0xA, 0xA), (0xD, 0xD), (0x20, 0xD7FF),
             (0xE000, 0xFFFD), (0x10000, 0x10FFFF)]
    ranges = "".join("%s-%s" % (chr(a), chr(b)) for a, b in valid)
    return re.compile("[^" + ranges + "]")


_XML_INVALID = _build_xml_invalid()


def _xesc(text):
    """Làm sạch ký tự lạ rồi escape sang XML an toàn."""
    return escape(_XML_INVALID.sub("", text))


# ---------------- Bộ dựng .docx (chỉ dùng stdlib) ----------------
class Docx:
    def __init__(self):
        self.body = []

    def _runs(self, text, bold_all=False):
        out = []
        for i, p in enumerate(text.split("**")):
            if p == "":
                continue
            b = bold_all or (i % 2 == 1)
            rpr = "<w:rPr>%s</w:rPr>" % ("<w:b/>" if b else "")
            out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                       % (rpr, _xesc(p)))
        if not out:
            out.append('<w:r><w:t xml:space="preserve"></w:t></w:r>')
        return "".join(out)

    def title(self, text):
        self.body.append('<w:p><w:pPr><w:pStyle w:val="TitleC"/></w:pPr>%s</w:p>'
                         % self._runs(text, bold_all=True))

    def heading(self, level, text):
        style = "Heading%d" % max(1, min(3, level))
        self.body.append('<w:p><w:pPr><w:pStyle w:val="%s"/></w:pPr>%s</w:p>'
                         % (style, self._runs(text)))

    def para(self, text="", space_after=120):
        ppr = '<w:pPr><w:spacing w:after="%d"/></w:pPr>' % space_after
        self.body.append('<w:p>%s%s</w:p>' % (ppr, self._runs(text)))

    def bullet(self, text):
        ppr = ('<w:pPr><w:spacing w:after="60"/>'
               '<w:ind w:left="620" w:hanging="260"/></w:pPr>')
        self.body.append('<w:p>%s%s</w:p>' % (ppr, self._runs("•  " + text)))

    def numbered(self, n, text):
        ppr = ('<w:pPr><w:spacing w:after="60"/>'
               '<w:ind w:left="620" w:hanging="360"/></w:pPr>')
        self.body.append('<w:p>%s%s</w:p>' % (ppr, self._runs("%d.  " % n + text)))

    def hr(self):
        self.body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" '
                         'w:space="1" w:color="BBBBBB"/></w:pBdr></w:pPr></w:p>')

    def table(self, rows, header=True):
        if not rows:
            return
        ncol = max(len(r) for r in rows)
        widths = [int(9400 / ncol)] * ncol
        grid = "".join('<w:gridCol w:w="%d"/>' % w for w in widths)
        borders = ('<w:tblBorders>'
                   '<w:top w:val="single" w:sz="4" w:color="888888"/>'
                   '<w:left w:val="single" w:sz="4" w:color="888888"/>'
                   '<w:bottom w:val="single" w:sz="4" w:color="888888"/>'
                   '<w:right w:val="single" w:sz="4" w:color="888888"/>'
                   '<w:insideH w:val="single" w:sz="4" w:color="888888"/>'
                   '<w:insideV w:val="single" w:sz="4" w:color="888888"/>'
                   '</w:tblBorders>')
        tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>%s'
                 '<w:tblLook w:val="04A0"/></w:tblPr>' % (sum(widths), borders))
        trs = []
        for ri, row in enumerate(rows):
            is_head = header and ri == 0
            shade = '<w:shd w:val="clear" w:fill="2E5D8A"/>' if is_head else ''
            tcs = []
            for ci in range(ncol):
                cell = row[ci] if ci < len(row) else ""
                w = widths[ci]
                if is_head:
                    runs = ('<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/></w:rPr>'
                            '<w:t xml:space="preserve">%s</w:t></w:r>' % _xesc(cell))
                else:
                    runs = self._runs(cell)
                tcpr = '<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>' % (w, shade)
                p = ('<w:p><w:pPr><w:spacing w:after="40" w:line="252" '
                     'w:lineRule="auto"/></w:pPr>%s</w:p>' % runs)
                tcs.append('<w:tc>%s%s</w:tc>' % (tcpr, p))
            trs.append('<w:tr>%s%s</w:tr>'
                       % (('<w:trPr><w:tblHeader/></w:trPr>' if is_head else ''),
                          "".join(tcs)))
        self.body.append('<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
                         % (tblpr, grid, "".join(trs)))
        self.para("", space_after=60)

    def save(self, path):
        doc_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body>' + "".join(self.body) +
            '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1418" '
            'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>'
            '</w:body></w:document>')
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="26"/><w:szCs w:val="26"/><w:lang w:val="vi-VN"/>'
            '</w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="276" '
            'w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="TitleC"><w:name w:val="TitleC"/>'
            '<w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="40"/><w:szCs w:val="40"/><w:color w:val="1F3F60"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:jc w:val="left"/>'
            '<w:spacing w:before="280" w:after="120"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="1F3F60"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:jc w:val="left"/>'
            '<w:spacing w:before="220" w:after="100"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="2E5D8A"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>'
            '<w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:jc w:val="left"/>'
            '<w:spacing w:before="160" w:after="80"/></w:pPr>'
            '<w:rPr><w:b/><w:i/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="333333"/></w:rPr></w:style>'
            '</w:styles>')
        ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '</Types>')
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                '</Relationships>')
        drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                 '</Relationships>')
        # Ghi ra file tạm rồi thay thế — tránh phá file cũ nếu lỗi giữa chừng
        # (hoặc khi file đang được Word mở).
        tmp_path = path + ".tmp"
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", ct)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/document.xml", doc_xml)
            z.writestr("word/styles.xml", styles_xml)
            z.writestr("word/_rels/document.xml.rels", drels)
        try:
            os.replace(tmp_path, path)
        except PermissionError:
            os.remove(tmp_path)
            raise PermissionError(
                "Không ghi được file Word — có thể bạn đang mở file này trong Word. "
                "Hãy đóng nó rồi chạy lại.")


# ---------------- Parser Markdown → Docx ----------------
def is_table_sep(line):
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def markdown_to_docx(md_text, out_path):
    d = Docx()
    lines = md_text.replace("\r\n", "\n").split("\n")
    i = 0
    n = len(lines)
    first_title_done = False
    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        # Bảng: dòng có '|' và dòng kế là dòng ngăn cách ---
        if "|" in line and i + 1 < n and is_table_sep(lines[i + 1]):
            rows = [split_row(line)]
            i += 2  # bỏ qua dòng header và dòng ngăn cách
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            d.table(rows, header=True)
            continue

        if not stripped:
            i += 1
            continue

        # Đường kẻ ngang
        if re.match(r"^\s*([-*_])\1{2,}\s*$", line):
            d.hr()
            i += 1
            continue

        # Tiêu đề
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            if level == 1 and not first_title_done:
                d.title(text)
                first_title_done = True
            else:
                d.heading(max(1, level - 1), text)
            i += 1
            continue

        # Danh sách đánh số
        m = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if m:
            d.numbered(int(m.group(1)), m.group(2).strip())
            i += 1
            continue

        # Gạch đầu dòng
        m = re.match(r"^[-*+]\s+(.*)$", stripped)
        if m:
            d.bullet(m.group(1).strip())
            i += 1
            continue

        # Đoạn văn thường
        d.para(stripped)
        i += 1

    d.save(out_path)


def main():
    if len(sys.argv) < 2:
        print("❌ Thiếu file biên bản.\n   Dùng: python make_bienban.py <file.md>")
        sys.exit(1)
    md_path = sys.argv[1]
    if os.path.isdir(md_path):
        print(f"❌ Đây là thư mục, không phải file: {md_path}")
        sys.exit(1)
    if not os.path.isfile(md_path):
        print(f"❌ Không tìm thấy file: {md_path}")
        sys.exit(1)

    # utf-8-sig: đọc được cả file có BOM (do Notepad trên Windows lưu)
    with open(md_path, "r", encoding="utf-8-sig") as f:
        md_text = f.read()

    if not md_text.strip():
        print("❌ File biên bản đang rỗng.")
        sys.exit(1)

    out_path = os.path.splitext(md_path)[0] + ".docx"
    try:
        markdown_to_docx(md_text, out_path)
    except PermissionError as e:
        print(f"❌ {e}")
        sys.exit(1)
    print("✅ Đã tạo file Word:")
    print(f"   {out_path}")


if __name__ == "__main__":
    main()
