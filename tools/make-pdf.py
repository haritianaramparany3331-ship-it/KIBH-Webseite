"""docs/prozessdokumentation.md -> a printable A4 PDF.

Same constraint as the rest of the project: no new dependencies. Playwright is
already here for the test suites, so Chromium does the typesetting and the PDF
export. The markdown subset handled is exactly the one the document uses.

    python tools/make-pdf.py                       # -> docs/Prozessdokumentation-KIBH.pdf
    python tools/make-pdf.py out.html out.pdf      # explicit paths

Run it through the Bash tool -- python.exe is not on the PowerShell PATH.
"""
import html
import pathlib
import re
import sys

SRC = pathlib.Path("docs/prozessdokumentation.md")
HTMLOUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("scratchpad-doc.html")
PDFOUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("docs/Prozessdokumentation-KIBH.pdf")

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
:root{
  --ink:#1c2226; --muted:#5a6570; --rule:#d8dee3; --accent:#4a8c8f;
  --accent-soft:#eef5f5; --warn:#8a5a00; --warn-soft:#fdf6e7;
}
*{box-sizing:border-box}
body{
  font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;
  font-size:9.7pt; line-height:1.5; color:var(--ink); margin:0;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
h1{
  font-size:20pt; line-height:1.18; margin:0 0 4mm; color:#12406b;
  letter-spacing:-0.01em;
}
h2{
  font-size:14pt; margin:0 0 4mm; padding:0 0 2mm;
  border-bottom:2.5px solid var(--accent); color:#12406b;
  break-after:avoid; page-break-after:avoid;
}
h2:not(:first-of-type){ break-before:page; page-break-before:always; margin-top:0; }
h3{
  font-size:11.2pt; margin:6mm 0 2mm; color:var(--accent);
  break-after:avoid; page-break-after:avoid;
}
h4{ font-size:10pt; margin:4mm 0 1.5mm; break-after:avoid; }
p{ margin:0 0 2.6mm; }
ul,ol{ margin:0 0 2.8mm; padding-left:5.2mm; }
li{ margin:0 0 1.3mm; }
li>ul,li>ol{ margin:1.3mm 0 0; }
strong{ font-weight:650; }
hr{ border:0; border-top:1px solid var(--rule); margin:6mm 0; }
a{ color:#12406b; text-decoration:none; word-break:break-word; }
code{
  font-family:"Cascadia Mono",Consolas,monospace; font-size:8.6pt;
  background:#f1f4f6; padding:0.4mm 1mm; border-radius:2px;
  word-break:break-word;
}
pre{
  background:#f7f9fa; border:1px solid var(--rule); border-left:3px solid var(--accent);
  padding:2.4mm 3mm; margin:0 0 3mm; overflow-x:auto;
  break-inside:avoid; page-break-inside:avoid;
}
pre code{ background:none; padding:0; font-size:8.4pt; line-height:1.42; }
blockquote{
  margin:0 0 3mm; padding:2mm 3mm; background:var(--accent-soft);
  border-left:3px solid var(--accent); color:#22343a;
}
blockquote p{ margin:0; }
table{
  width:100%; border-collapse:collapse; margin:0 0 3.4mm; font-size:8.9pt;
  break-inside:avoid; page-break-inside:avoid;
}
th,td{ border:1px solid var(--rule); padding:1.5mm 2mm; text-align:left; vertical-align:top; }
th{ background:var(--accent-soft); font-weight:650; }
tr:nth-child(even) td{ background:#fbfcfd; }
/* the review markers */
.mark{
  display:inline-block; background:var(--warn-soft); border:1px solid #e8d9b0;
  border-left:3px solid var(--warn); padding:1.2mm 2mm; border-radius:2px;
  color:#4a3a12; font-size:9.1pt;
}
.mark code{ background:#f3ead4; }
.lead{ color:var(--muted); }
.meta{
  border:1px solid var(--rule); border-left:3px solid var(--accent);
  background:#fbfcfd; padding:3mm; margin:0 0 5mm; font-size:9.2pt;
}
.meta p{ margin:0 0 1.4mm; } .meta p:last-child{ margin:0; }
"""

FENCE = re.compile(r"^```")


def inline(t: str) -> str:
    """Escape, then re-introduce the inline markup the document uses.

    Code spans are parked behind a sentinel rather than converted up front:
    bold frequently wraps one (`**`CLAUDE.md` anlegen**`), and splitting on the
    backticks first would put the opening and closing `**` in different pieces,
    so neither ever matched and the asterisks printed literally.
    """
    spans = []

    def park(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    s = re.sub(r"`([^`]+)`", park, t)
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"(https?://[^\s<),]+)", r'<a href="\1">\1</a>', s)
    # highlight the review markers -- opening and closing tag in one pass, so
    # the span can never be left unbalanced
    s = re.sub(
        r"\[((?:korrigiert|gemessen|Hinweis|Präzisierung|Anmerkung|ergänzt|Belege?)"
        r"[^:\]]*:[^\]]*)\]",
        r'<span class="mark">[\1]</span>', s)
    # put the code spans back, escaped
    s = re.sub(r"\x00(\d+)\x00",
               lambda m: "<code>" + html.escape(spans[int(m.group(1))]) + "</code>", s)
    return s


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def convert(md: str) -> str:
    lines = md.split("\n")
    out, i, n = [], 0, len(lines)
    list_stack = []  # (tag, indent)

    def close_lists(to_indent=-1):
        while list_stack and list_stack[-1][1] > to_indent:
            out.append(f"</{list_stack.pop()[0]}>")

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if FENCE.match(stripped):
            i += 1
            buf = []
            while i < n and not FENCE.match(lines[i].strip()):
                buf.append(lines[i]); i += 1
            i += 1
            close_lists()
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            continue

        if not stripped:
            i += 1
            continue

        if stripped.startswith("---") and set(stripped) == {"-"}:
            close_lists(); out.append("<hr>"); i += 1; continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            close_lists()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        if stripped.startswith("|"):
            close_lists()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            body = [r for r in cells if not all(set(c) <= set("-: ") and c for c in r)]
            head = body[0] if body else []
            out.append("<table><thead><tr>"
                       + "".join(f"<th>{inline(c)}</th>" for c in head)
                       + "</tr></thead><tbody>")
            for r in body[1:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue

        if stripped.startswith(">"):
            close_lists()
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue

        ind = indent_of(line)
        mb = re.match(r"^[-*]\s+(.*)$", stripped)
        mo = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if mb or mo:
            tag = "ul" if mb else "ol"
            text = mb.group(1) if mb else mo.group(2)
            while list_stack and list_stack[-1][1] > ind:
                out.append(f"</{list_stack.pop()[0]}>")
            # an <ol> interrupted by a code block or paragraph must resume its
            # numbering, not restart at 1 -- the markdown carries the real number
            startattr = f' start="{mo.group(1)}"' if mo else ""
            if not list_stack or list_stack[-1][1] < ind:
                list_stack.append((tag, ind)); out.append(f"<{tag}{startattr}>")
            elif list_stack[-1][0] != tag:
                out.append(f"</{list_stack.pop()[0]}>")
                list_stack.append((tag, ind)); out.append(f"<{tag}{startattr}>")
            # gather continuation lines (deeper indent, not a new bullet)
            i += 1
            cont = [text]
            while i < n:
                nxt = lines[i]
                if not nxt.strip(): break
                if re.match(r"^\s*([-*]|\d+\.)\s+", nxt): break
                if indent_of(nxt) <= ind and nxt.strip(): break
                if FENCE.match(nxt.strip()): break
                cont.append(nxt.strip()); i += 1
            out.append("<li>" + inline(" ".join(cont)) + "</li>")
            continue

        close_lists()
        buf = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^\s*(#{1,4}\s|[-*]\s|\d+\.\s|\||>|```|---\s*$)", lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")

    close_lists()
    return "\n".join(out)


md = SRC.read_text(encoding="utf-8")
body = convert(md)
doc = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Prozessdokumentation — KIBH</title><style>{CSS}</style></head>
<body>{body}</body></html>"""
HTMLOUT.write_text(doc, encoding="utf-8")

from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(HTMLOUT.resolve().as_uri(), wait_until="networkidle")
    pg.pdf(
        path=str(PDFOUT), format="A4", print_background=True,
        margin={"top": "18mm", "bottom": "20mm", "left": "16mm", "right": "16mm"},
        display_header_footer=True,
        header_template='<div style="width:100%"></div>',
        footer_template=(
            '<div style="width:100%;font-family:Segoe UI,Arial,sans-serif;font-size:7.5pt;'
            'color:#7a848c;padding:0 16mm;display:flex;justify-content:space-between">'
            '<span>Prozessdokumentation — KIBH-Migration mit Claude Code</span>'
            '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'),
    )
    b.close()
print(f"HTML: {HTMLOUT}  ({HTMLOUT.stat().st_size//1024} KB)")
print(f"PDF : {PDFOUT}   ({PDFOUT.stat().st_size//1024} KB)")
