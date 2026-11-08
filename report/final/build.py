#!/usr/bin/env python3
"""Build the final report. Converts the appendices from report/final/appendices.md to LaTeX, then runs tectonic.

Run from the repo root: python3 report/final/build.py
Writes NST2046_MS2_Report_with_ids.pdf (git-ignored, for submission, needs ids.tex) and NST2046_MS2_Report.pdf
(public copy with the ID column left blank).
"""
import pathlib
import re
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"
BUILD.mkdir(exist_ok=True)


def esc(s: str) -> str:
    out = []
    for ch in s:
        out.append({"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
                    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}.get(ch, ch))
    return "".join(out)


def inline(s: str) -> str:
    """Escape text and convert `code`, **bold**, *italic*, links and team flags."""
    tokens, s2 = [], s

    def stash(tex):
        tokens.append(tex)
        return f"\x00{len(tokens) - 1}\x00"

    def code(m):
        body = esc(m.group(1)).replace(r"\_", r"\_\allowbreak{}").replace("/", r"/\allowbreak{}").replace("-", r"-\allowbreak{}")
        return stash(r"\texttt{" + body + "}")

    s2 = re.sub(r"`([^`]+)`", code, s2)
    s2 = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: stash(r"\href{" + m.group(2).replace("%", r"\%").replace("#", r"\#") + "}{" + esc(m.group(1)) + "}"), s2)
    s2 = re.sub(r"(?<![\w(])(https?://[^\s|)]+)", lambda m: stash(r"\url{" + m.group(1).replace("%", r"\%").replace("#", r"\#") + "}"), s2)
    s2 = re.sub(r"\[(TEAM TO (?:COMPLETE|READ)[^\]]*|CHECK SOURCE)\]", lambda m: stash(r"\todo{" + esc(m.group(1)) + "}"), s2)
    s2 = esc(s2)
    s2 = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s2)
    s2 = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"\\emph{\1}", s2)
    s2 = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], s2)
    return s2


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def table(rows: list[str]) -> str:
    head, body = cells(rows[0]), [cells(r) for r in rows[2:]]
    n = len(head)
    body = [(r + [""] * n)[:n] for r in body]
    weights = [max(6, min(60, (sum(len(r[i]) for r in body) / max(1, len(body))) ** 0.75)) for i in range(n)]
    # Every column is at least as wide as its longest word, so no word sticks out of its cell.
    plain = lambda c: re.sub(r"`[^`]*`|https?://\S+|[*\[\]()]", " ", c)  # noqa: E731
    longest = [max((len(w) for r in [head] + body for w in plain(r[i]).split()), default=4) for i in range(n)]
    floors = [min(0.30, (ln * 5.1 + 12) / 495) for ln in longest]
    widths = [w / sum(weights) for w in weights]
    for _ in range(4):
        widths = [max(w, fl) for w, fl in zip(widths, floors)]
        widths = [w / sum(widths) for w in widths]
    # Wider text columns are justified like the body. Narrow columns stay left-aligned, because justifying them leaves large gaps.
    align = lambda w: r"\justifying" if w >= 0.34 else r"\RaggedRight"  # noqa: E731
    spec = "".join(">{" + align(w) + r"\arraybackslash}p{" + f"{w * 0.985:.3f}" + r"\dimexpr\linewidth-" + f"{2 * n}" + r"\tabcolsep\relax}" for w in widths)
    lines = [r"\begin{longtable}{@{}" + spec + "@{}}", r"\toprule", " & ".join(r"\textbf{" + inline(h) + "}" for h in head) + r" \\",
             r"\midrule", r"\endhead"]
    lines += [" & ".join(inline(c) for c in r) + r" \\" for r in body]
    lines += [r"\bottomrule", r"\end{longtable}"]
    return r"{\small" + "\n" + "\n".join(lines) + "\n}"


def convert(md: str) -> str:
    out, i, ls = [], 0, md.split("\n")
    while i < len(ls):
        line = ls[i]
        if line.startswith("```"):
            i += 1
            block = []
            while not ls[i].startswith("```"):
                block.append(ls[i])
                i += 1
            i += 1
            out.append(r"\begin{lstlisting}" + "\n" + "\n".join(block) + "\n" + r"\end{lstlisting}")
        elif line.startswith("## "):
            out.append(r"\section*{" + inline(line[3:]) + "}\n" + r"\addcontentsline{toc}{section}{" + inline(line[3:]) + "}")
            i += 1
        elif line.startswith("### "):
            out.append(r"\subsection*{" + inline(line[4:]) + "}")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(ls) and ls[i].startswith("|"):
                rows.append(ls[i])
                i += 1
            out.append(table(rows))
        elif line.startswith("- "):
            items = []
            while i < len(ls) and ls[i].startswith(("- ", "  ")):
                if ls[i].startswith("- "):
                    items.append(ls[i][2:])
                else:
                    items[-1] += " " + ls[i].strip()
                i += 1
            out.append(r"\begin{itemize}[leftmargin=12pt,itemsep=1pt,topsep=2pt]" + "\n" + "\n".join(r"\item " + inline(x) for x in items) + "\n" + r"\end{itemize}")
        elif line.strip():
            para = [line]
            i += 1
            while i < len(ls) and ls[i].strip() and not ls[i].startswith(("|", "#", "```", "- ")):
                para.append(ls[i])
                i += 1
            out.append(inline(" ".join(para)))
        else:
            i += 1
    return "\n\n".join(out)


def compile_pdf(with_ids: bool) -> pathlib.Path:
    name = "NST2046_MS2_Report_with_ids" if with_ids else "NST2046_MS2_Report"
    ids = (HERE / "ids.tex").read_text() if with_ids and (HERE / "ids.tex").exists() else (
        "\\newcommand{\\idAditya}{}\\newcommand{\\idAdvaith}{}\\newcommand{\\idTony}{}\\newcommand{\\idElkan}{}\n")
    (BUILD / "ids_used.tex").write_text(ids)
    src = (HERE / "main.tex").read_text()
    (HERE / f"{name}.tex").write_text(src)
    try:
        subprocess.run(["tectonic", "-Z", "search-path=build", "--keep-logs", "--outdir", str(BUILD), str(HERE / f"{name}.tex")],
                       cwd=HERE, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr[-3000:])
        raise
    finally:
        (HERE / f"{name}.tex").unlink()
    shutil.copy(BUILD / f"{name}.pdf", HERE / f"{name}.pdf")
    return HERE / f"{name}.pdf"


if __name__ == "__main__":
    (BUILD / "appendices.tex").write_text(convert((HERE / "appendices.md").read_text()))
    for flag in (True, False):
        print("wrote", compile_pdf(flag))
