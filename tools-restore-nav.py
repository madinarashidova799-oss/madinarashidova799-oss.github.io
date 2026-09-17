#!/usr/bin/env python3
"""Вернуть нижнюю навигацию кейсов к состоянию запущенной версии (git HEAD).

Берёт из HEAD дословно: CSS-блок фиксированного дока, правила соседних
кнопок, медиазапросы и саму разметку <nav class="case-floating-nav">.
Ничего не переписывает и не «улучшает».

После восстановления компонент не редактируется: остальные скрипты сборки
трогают только содержимое <div class="case-page">.
"""
import pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
FILES = ["case-alif-partners.html", "case-eaj-trader.html",
         "case-namaste.html", "case-360-tracker.html"]

# Границы CSS-области навигации в исходном файле.
CSS_FROM = "  .case-floating-nav {"
CSS_TO = "\n\n  /* ===== "          # начало следующего именованного блока
# В текущем файле область начинается уже с кнопок — дока в ней нет.
CUR_FROM_CANDIDATES = ("  .case-floating-nav {", "  .case-next, .case-prev {",
                       "  .case-next, .case-home {")


def head(fname):
    return subprocess.run(["git", "show", f"HEAD:{fname}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def css_region(text):
    """CSS навигации: от дока до начала следующего именованного блока.

    Раньше границей служил только </style>. Пока в HEAD после правил дока
    ничего не было, это совпадало; как только блок «Редакция» попал в
    коммит, скрипт стал вклеивать его вместе с навигацией и удваивал при
    каждом прогоне. Граница теперь одна и та же с обеих сторон.
    """
    start = text.index(CSS_FROM)
    marker = text.find(CSS_TO.strip("\n"), start)
    end = marker if marker != -1 else text.index("</style>", start)
    return start, end


def main():
    for f in FILES:
        src = head(f)
        p = ROOT / f
        cur = p.read_text()

        s0, s1 = css_region(src)
        # Ровно одна пустая строка до следующего блока, сколько бы раз
        # скрипт ни запускали: иначе каждый прогон добавлял по строке.
        block = src[s0:s1].rstrip("\n") + "\n\n"

        cur_start = next(cur.index(c) for c in CUR_FROM_CANDIDATES if c in cur)
        cur_end = cur.index("  /* ===== Редакция", cur_start)
        cur = cur[:cur_start] + block + cur[cur_end:]

        nav = re.search(r'<nav class="case-(?:floating|footer)-nav">.*?</nav>', cur, re.S)
        orig_nav = re.search(r'<nav class="case-floating-nav">.*?</nav>', src, re.S).group(0)
        cur = cur[:nav.start()] + orig_nav + cur[nav.end():]
        p.write_text(cur)

        ok = ('<nav class="case-floating-nav">' in cur
              and ".case-floating-nav {" in cur
              and "case-footer-nav" not in cur)
        print(f, "| восстановлена:", ok)

    # скрипт дока — тоже из HEAD
    js = ROOT / "assets/case-nav.js"
    js.write_text(head("assets/case-nav.js"))
    print("assets/case-nav.js | восстановлен из HEAD")


main()
