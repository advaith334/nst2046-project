"""Build report.pdf from report.md. Run: uv run --no-project --python 3.12 --with markdown --with weasyprint python report/draft/build_pdf.py report/draft/report.md report/draft/report.pdf"""
import re,sys,pathlib,markdown,weasyprint
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
t=src.read_text()
html=markdown.markdown(t,extensions=['tables','attr_list','sane_lists','fenced_code','md_in_html'])
# captions
html=re.sub(r'<p><strong>((?:Figure|Table) [0-9A-Z]+\.)</strong>',r'<p class="cap"><strong>\1</strong>',html)
# figure paragraphs
html=re.sub(r'<p>(<img [^>]*>)</p>',r'<p class="fig">\1</p>',html)
html=re.sub(r'\[((?:TEAM TO (?:COMPLETE|READ))[^\]]*|CHECK SOURCE)\]',r'<mark>[\1]</mark>',html)
a=html.index('<h2>References</h2>'); b=html.index('<h2>Appendix A')
html=html[:a]+'<div class="refs" style="break-before:page">'+html[a:b]+'</div><div class="appendix" style="break-before:page">'+html[b:]+'</div>'
html=re.sub(r'<h2>(Appendix [B-F])',r'<h2 style="break-before:page">\1',html)
css='''
@page{size:A4;margin:19mm 19mm 18mm 19mm;@bottom-center{content:counter(page);font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:8.5pt;color:#555}}
html{font-family:"Georgia","Times New Roman",serif;font-size:10pt;line-height:1.36;color:#111}
body{margin:0}
h1{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:19pt;margin:0 0 2pt;line-height:1.15}
.subtitle{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:11pt;margin:0 0 4pt;color:#333}
.byline{font-size:9pt;margin:0 0 7pt;color:#333}
h2{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:12pt;margin:11pt 0 3pt;break-after:avoid}
h3{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:10.5pt;margin:8pt 0 2pt;break-after:avoid}
p{margin:0 0 5pt;text-align:left;orphans:2;widows:2}
blockquote{margin:0 0 8pt;padding:6pt 9pt;border:1.2pt solid #b3261e;background:#fdf1f0;font-size:9.2pt}
blockquote p{margin:0}
mark{background:#ffe680;padding:0 1pt}
img{width:100%;display:block}
p.fig{margin:5pt 0 2pt;break-after:avoid;text-align:center}
p.fig img{width:72%;margin:0 auto}
p.cap{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:8.3pt;line-height:1.28;color:#222;margin:2pt 0 7pt}
p.cap:has(+ table){break-after:avoid;margin-bottom:2pt}
p:has(+ table){break-after:avoid}
table{border-collapse:collapse;width:100%;font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:7.9pt;line-height:1.2;margin:0 0 7pt}
th{border-top:.9pt solid #111;border-bottom:.6pt solid #111;text-align:left;padding:2pt 3pt;vertical-align:bottom}
td{border-bottom:.3pt solid #bbb;padding:1.6pt 3pt;vertical-align:top}
thead{display:table-header-group}
tr{break-inside:avoid}
code{font-family:"Menlo","Courier New",monospace;font-size:88%}
pre{font-family:"Menlo","Courier New",monospace;font-size:7.4pt;line-height:1.25;background:#f5f5f5;padding:4pt 5pt;white-space:pre-wrap;margin:0 0 6pt}
pre code{font-size:100%}
.appendix table{font-size:7.1pt}
.appendix h2{font-size:12pt;margin-top:12pt}
.refs p{font-size:8.7pt;line-height:1.28;margin-bottom:2.4pt;padding-left:12pt;text-indent:-12pt}
'''
doc=f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>When a Memory Counts as Evidence</title><style>{css}</style></head><body>{html}</body></html>'
weasyprint.HTML(string=doc,base_url=str(src.parent)+'/').write_pdf(str(out))
