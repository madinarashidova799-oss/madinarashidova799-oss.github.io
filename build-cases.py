#!/usr/bin/env python3
"""Собрать четыре страницы кейсов из утверждённого текста.

Источник: content.json (RU, редакция 3.1) + content.en.json (EN, перевод).
Оба файла хранят не только текст, но и композицию каждого блока (поле layout),
поэтому отдельного файла разметки нет.

Скрипт заменяет только содержимое <div class="case-page"> и не трогает
шапку, верхнюю навигацию, лайтбокс, нижний док переходов и <style> страниц.
Запуск из корня репозитория: python3 build-cases.py
"""
import json, pathlib, re, subprocess, html

ROOT = pathlib.Path(__file__).resolve().parent

PAGES = {"alif": "case-alif-partners.html", "eaj": "case-eaj-trader.html",
         "namaste": "case-namaste.html", "tracker": "case-360-tracker.html"}

# id материала -> файл репозитория без языкового суффикса.
# Сопоставлено по содержимому картинок, не по именам (см. ASSET-MAP.md).
ASSETS = {
 "AL-01": "assets/process/alif-research-table",   "AL-02": "assets/process/alif-admin-structure",
 "AL-03": "assets/process/alif-chat",             "AL-04": "assets/process/alif-notifications",
 "AL-05": "assets/process/alif-product-search",   "AL-06": "assets/process/alif-price-insight",
 "AL-07": "assets/process/alif-delivery",         "AL-09": "assets/process/alif-mobile",
 "EA-01": "assets/process/eaj-research",          "EA-02": "assets/process/eaj-home",
 "EA-03": "assets/process/eaj-funding-2",         "EA-04": "assets/process/eaj-claims-list",
 # Имена файлов концептов обманывают: eaj-concept1 — карточки, eaj-concept2 —
 # таблица. Сопоставлено по содержимому (см. ASSET-MAP.md).
 "EA-05": "assets/process/eaj-claims-detail",     "EA-06": "assets/process/eaj-concept2",
 "EA-07": "assets/process/eaj-concept1",
 "NA-01": "assets/namaste/Research",              "NA-02": "assets/Userflow",
 "TR-01": "assets/process/tracker-userflow",      "TR-02": "assets/process/tracker-main",
 "TR-03": "assets/process/tracker-geofence-main", "TR-04": "assets/process/tracker-privacy-main",
 "TR-05": "assets/process/tracker-history",       "TR-06": "assets/process/tracker-final",
}

# Пары светлая/тёмная тема для слайдера Namaste.
THEME_PAIRS = {
 "уровень": ("assets/namaste/уровень-white", "assets/namaste/уровень-dark"),
 "фокус":   ("assets/namaste/фокус-white",   "assets/namaste/фокус-dark"),
 "Финал":   ("assets/namaste/Финал-white",   "assets/namaste/Финал-dark"),
}

# TR-07 и TR-08 в исходной редакции — картинки таблиц сравнения конкурентов.
# На сайте эти же данные уже есть настоящими двуязычными <table>: они
# читаются скринридером, переводятся вместе со страницей и не требуют
# увеличения. Картинку заменяем таблицей, содержимое совпадает построчно.
TABLE_FOR_ASSET = {"TR-07": 0, "TR-08": 1}
TRACKER_TABLES = (ROOT / "tracker_tables.html").read_text().split("\n<!--SPLIT-->\n")

META_EN = {"Срок": "Duration", "Роль": "Role", "Платформы": "Platforms", "Команда": "Team"}
OPEN = ("Открыть изображение", "Open image")
MEASURE = ("Влияние оценивали по", "Impact was evaluated using")
CTX = (("context", "Контекст", "Context"), ("task", "Задача", "Task"))

ru_doc = json.load(open(ROOT / "content.json"))
en_cases = {c["id"]: c for c in json.load(open(ROOT / "content.en.json"))["cases"]}

_dims = {}
def dims(path):
    if path not in _dims:
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(ROOT / path)],
                           capture_output=True, text=True).stdout
        _dims[path] = (int(re.search(r"pixelWidth: (\d+)", o).group(1)),
                       int(re.search(r"pixelHeight: (\d+)", o).group(1)))
    return _dims[path]

def esc(s): return html.escape(s, quote=True)
def bl(ru, en): return f'<span data-lang="ru">{ru}</span><span data-lang="en">{en}</span>'

def srcs(stem):
    ru, en = f"{stem}-ru.webp", f"{stem}.webp"
    if not (ROOT / ru).exists(): ru = en
    if not (ROOT / en).exists(): en = ru
    assert (ROOT / ru).exists(), stem
    return ru, en

_fig_n = [0]


def figure(rf, ef, indent, extra=""):
    """Кадр с интерфейсом. Подпись вынесена из белого контейнера: она идёт
    строкой под ним и не увеличивает его высоту. Сам контейнер кликабелен
    мышью, а в табуляцию попадает одна подписанная кнопка «Открыть
    изображение» — так у клавиатуры на каждую картинку ровно один понятный
    элемент управления вместо безымянной кнопки-картинки."""
    _fig_n[0] += 1
    fid = f'fig-{rf["asset"].lower()}-{_fig_n[0]}'
    ru_src, en_src = srcs(ASSETS[rf["asset"]])
    w, h = dims(ru_src)
    p = " " * indent
    cls = "case-fig" + (f" {extra}" if extra else "")
    return (f'{p}<figure class="{cls}">\n'
            f'{p}  <div class="case-shot" data-lightbox-for="{fid}">\n'
            f'{p}    <img id="{fid}" data-src-ru="{ru_src}" data-src-en="{en_src}"'
            f' data-alt-ru="{esc(rf["alt"])}" data-alt-en="{esc(ef["alt"])}"'
            f' alt="{esc(rf["alt"])}" loading="lazy" width="{w}" height="{h}">\n'
            f'{p}  </div>\n'
            f'{p}  <figcaption class="case-fig__cap">'
            f'<span class="case-fig__text">{bl(esc(rf["caption"]), esc(ef["caption"]))}</span>'
            f'<button type="button" class="case-fig__open" data-lightbox-for="{fid}">'
            f'{bl(*OPEN)}</button></figcaption>\n'
            f'{p}</figure>')

def aspect(rf):
    ru_src, _ = srcs(ASSETS[rf["asset"]])
    w, h = dims(ru_src)
    return w / h

def split_cols(rf):
    """Ширина колонок выбирается по пропорции экрана: вертикальный экран
    читается в половине сетки, широкий интерфейс — нет."""
    a = aspect(rf)
    if a < 1.05: return "col-6", "col-6"
    if a < 1.8:  return "col-5", "col-7"
    return "col-4", "col-8"

def table_html(rt, et, indent, narrow=False, label=None):
    p = " " * indent
    head = "".join(f'<th scope="col">{bl(esc(r), esc(e))}</th>'
                   for r, e in zip(rt["headers"], et["headers"]))
    rows = ""
    for rr, er in zip(rt["rows"], et["rows"]):
        cells = f'<th scope="row">{bl(esc(rr[0]), esc(er[0]))}</th>'
        cells += "".join(f"<td>{bl(esc(a), esc(b))}</td>" for a, b in zip(rr[1:], er[1:]))
        rows += f"\n{p}      <tr>{cells}</tr>"
    cls = "case-table-wrap" + (" case-table-wrap--narrow" if narrow else "")
    # role="region" без имени — безымянная область в дереве доступности. Имя
    # берём из заголовка секции; aria-label — атрибут, пары <span data-lang>
    # в него не положить, поэтому язык переключает i18n.js по data-aria-*.
    lru, len_ = label or ("Таблица", "Table")
    aria = (f' aria-label="{esc(lru)}: таблица"'
            f' data-aria-ru="{esc(lru)}: таблица" data-aria-en="{esc(len_)}: table"')
    return (f'{p}<div class="{cls}" tabindex="0" role="region"{aria}>\n'
            f'{p}  <table class="case-table">\n'
            f'{p}    <thead><tr>{head}</tr></thead>\n'
            f'{p}    <tbody>{rows}\n{p}    </tbody>\n'
            f'{p}  </table>\n{p}</div>')

def slider(pair, rf_alt, ef_alt, indent):
    white, dark = THEME_PAIRS[pair]
    wru, wen = srcs(white); dru, den = srcs(dark)
    ww, wh = dims(wru)
    p = " " * indent
    sid = f"theme-{pair}"
    return "\n".join([
      f'{p}<div class="compare-slider__frame">',
      f'{p}  <div class="compare-slider__stage" data-compare-slider>',
      f'{p}    <img class="compare-slider__base" id="{sid}-light" data-src-ru="{wru}" data-src-en="{wen}"'
      f' data-alt-ru="{esc(rf_alt)}, светлая тема" data-alt-en="{esc(ef_alt)}, light theme"'
      f' alt="{esc(rf_alt)}, светлая тема" loading="lazy" width="{ww}" height="{wh}">',
      f'{p}    <div class="compare-slider__overlay">',
      f'{p}      <img id="{sid}-dark" data-src-ru="{dru}" data-src-en="{den}"'
      f' data-alt-ru="{esc(rf_alt)}, тёмная тема" data-alt-en="{esc(ef_alt)}, dark theme"'
      f' alt="{esc(rf_alt)}, тёмная тема" loading="lazy" width="{ww}" height="{wh}">',
      f'{p}    </div>',
      f'{p}    <span class="compare-slider__tag compare-slider__tag--left">{bl("Светлая", "Light")}</span>',
      f'{p}    <span class="compare-slider__tag compare-slider__tag--right">{bl("Тёмная", "Dark")}</span>',
      f'{p}    <div class="compare-slider__handle"><span class="compare-slider__grip" aria-hidden="true">‹›</span></div>',
      f'{p}    <input class="compare-slider__range" type="range" min="0" max="100" value="50" step="1"'
      f' aria-label="{esc(rf_alt)}: сравнение светлой и тёмной темы"'
      f' data-aria-ru="{esc(rf_alt)}: сравнение светлой и тёмной темы"'
      f' data-aria-en="{esc(ef_alt)}: light and dark theme comparison">',
      f'{p}  </div>',
      f'{p}  <div class="compare-slider__tools">',
      f'{p}    <span class="compare-slider__hint">{bl("Перетащите разделитель или используйте стрелки", "Drag the divider or use the arrow keys")}</span>',
      f'{p}    <span class="compare-slider__zooms">',
      f'{p}      <button type="button" class="compare-slider__zoom" data-lightbox-for="{sid}-light">{bl("Светлая крупно", "Light, full size")}</button>',
      f'{p}      <button type="button" class="compare-slider__zoom" data-lightbox-for="{sid}-dark">{bl("Тёмная крупно", "Dark, full size")}</button>',
      f'{p}    </span>',
      f'{p}  </div>',
      f'{p}</div>'])


def render_block(rb, eb, L, state):
    t = rb["type"]

    def paragraphs(indent):
        return [f'{" " * indent}<p>{bl(esc(a), esc(b))}</p>'
                for a, b in zip(rb.get("paragraphs", []), eb.get("paragraphs", []))]

    def subhead(indent):
        """Заголовок текстового блока. Если заголовок секции не вынесен
        наверх, он идёт здесь же — заголовок и абзац должны читаться как
        один модуль, а не как два разных элемента секции."""
        out = []
        p = " " * indent
        if state.pop("head_in_column", None):
            out.append(f'{p}<h2 class="case-lead-title">'
                       f'{bl(esc(state["sec_title_ru"]), esc(state["sec_title_en"]))}</h2>')
        if "subhead" in rb:
            tag = "h3" if out else "h3"
            out.append(f'{p}<{tag} class="case-subhead">{bl(esc(rb["subhead"]), esc(eb["subhead"]))}</{tag}>')
        return out

    def points(indent):
        """Два-три коротких вывода под абзацем, в той же колонке."""
        if not rb.get("points"): return []
        p = " " * indent
        out = [f'{p}<ul class="case-points">']
        for ri, ei in zip(rb["points"], eb["points"]):
            out += [f'{p}  <li>',
                    f'{p}    <p class="case-points__title">{bl(esc(ri["title"]), esc(ei["title"]))}</p>',
                    f'{p}    <p class="case-points__text">{bl(esc(ri["text"]), esc(ei["text"]))}</p>',
                    f'{p}  </li>']
        out.append(f'{p}</ul>')
        return out

    if t == "subhead":
        L.append(f'        <h3 class="case-subhead">{bl(esc(rb["text"]), esc(eb["text"]))}</h3>')

    elif t == "lede":
        L += subhead(8) + paragraphs(8)

    elif t == "rail":
        L.append(f'        <ol class="case-rail" style="--rail-cols: {len(rb["steps"])}">')
        for i, (rs, es) in enumerate(zip(rb["steps"], eb["steps"]), 1):
            L += ['          <li class="case-rail__step">',
                  f'            <span class="case-rail__num" aria-hidden="true">{i}</span>',
                  f'            <h3 class="case-rail__title">{bl(esc(rs["title"]), esc(es["title"]))}</h3>',
                  f'            <p class="case-rail__text">{bl(esc(rs["text"]), esc(es["text"]))}</p>',
                  '          </li>']
        L.append('        </ol>')

    elif t in ("notes", "insights"):
        items = list(zip(rb["items"], eb["items"]))
        cls = "case-cols" + (" case-cols--compact" if rb.get("compact") else "")
        L.append(f'        <div class="{cls}" style="--cols: {len(items)}">')
        for ri, ei in items:
            L.append('          <div class="case-col">')
            if "label" in ri:
                L.append(f'            <p class="case-col__label">{bl(esc(ri["label"]), esc(ei["label"]))}</p>')
            L += [f'            <h3 class="case-col__title">{bl(esc(ri["title"]), esc(ei["title"]))}</h3>',
                  f'            <p class="case-col__text">{bl(esc(ri["text"]), esc(ei["text"]))}</p>',
                  '          </div>']
        L.append('        </div>')

    elif t == "split":
        figs = list(zip(rb.get("figures", []), eb.get("figures", [])))
        tables = [f for f in figs if f[0]["asset"] in TABLE_FOR_ASSET]
        figs = [f for f in figs if f[0]["asset"] not in TABLE_FOR_ASSET]
        layout = rb.get("layout", "even")

        def after_paras(indent):
            return [f'{" " * indent}<p>{bl(esc(a), esc(b))}</p>'
                    for a, b in zip(rb.get("after", []), eb.get("after", []))]

        def media(indent, extra=""):
            out = []
            if len(figs) >= 2:
                out.append(f'{" " * indent}<div class="case-figs case-figs--stack">')
                for rf, ef in figs: out.append(figure(rf, ef, indent + 2, extra=extra))
                out.append(f'{" " * indent}</div>')
            elif figs:
                out.append(figure(*figs[0], indent, extra=extra))
            return out

        if layout == "center8":
            # Вступление в 6 колонок, таблица или схема — в 8 по центру.
            state.pop("head_in_column", None)
            if rb.get("subhead") or rb.get("paragraphs"):
                L.append('        <div class="case-grid">')
                L.append('          <div class="case-split-text col-6">')
                L += subhead(12) + paragraphs(12)
                L.append('          </div>')
                L.append('        </div>')
            plain = " case-fig--plain" if rb.get("plain") else ""
            if figs or tables:
                L.append('        <div class="case-grid">')
                L.append('          <div class="col-8-center">')
                L += media(12, extra=plain.strip())
                for rf, ef in tables:
                    L.append(f'            <p class="case-artifact-cap">{bl(esc(rf["caption"]), esc(ef["caption"]))}</p>')
                    L.append(TRACKER_TABLES[TABLE_FOR_ASSET[rf["asset"]]].rstrip("\n"))
                L.append('          </div>')
                L.append('        </div>')
            if "table" in rb:
                L.append('        <div class="case-grid">')
                L.append('          <div class="col-8-center">')
                L.append(table_html(rb["table"], eb["table"], 12, label=(state["sec_title_ru"], state["sec_title_en"])))
                L.append('          </div>')
                L.append('        </div>')
            if rb.get("after"):
                L.append('        <div class="case-grid">')
                L.append('          <div class="col-8-center">')
                L.append('            <div class="case-takeaway">')
                L += after_paras(14)
                L.append('            </div>')
                L.append('          </div>')
                L.append('        </div>')
        else:
            tc, mc = ("col-4", "col-8") if layout == "accent" else ("col-6", "col-6")
            cls = "case-grid case-split"
            if rb.get("media_first"): cls += " case-split--flip"
            L.append(f'        <div class="{cls}">')
            L.append(f'          <div class="case-split-text {tc}">')
            L += subhead(12) + paragraphs(12) + points(12)
            L.append('          </div>')
            L.append(f'          <div class="{mc}">')
            L += media(12)
            if rb.get("captions"):
                L.append('            <ul class="case-shot-labels" style="--cols: %d">'
                         % len(rb["captions"]))
                for cr, ce in zip(rb["captions"], eb["captions"]):
                    L.append(f'              <li>{bl(esc(cr), esc(ce))}</li>')
                L.append('            </ul>')
            L.append('          </div>')
            L.append('        </div>')
            for rf, ef in tables:
                L.append(f'        <p class="case-artifact-cap">{bl(esc(rf["caption"]), esc(ef["caption"]))}</p>')
                L.append(TRACKER_TABLES[TABLE_FOR_ASSET[rf["asset"]]].rstrip("\n"))
            if "table" in rb:
                L.append(table_html(rb["table"], eb["table"], 8, narrow=True, label=(state["sec_title_ru"], state["sec_title_en"])))
            if rb.get("after"):
                L.append('        <div class="case-takeaway">')
                L += after_paras(10)
                L.append('        </div>')

    elif t == "sequence":
        # Один сценарий по шагам. Каждый шаг — та же сетка 4/8, что и в
        # акцентных секциях: картинка не выходит за 8 колонок.
        L.append('        <ol class="case-seq">')
        for i, (rs, es) in enumerate(zip(rb["steps"], eb["steps"]), 1):
            L.append('          <li class="case-seq__step case-grid">')
            L.append('            <div class="case-seq__head col-4">')
            L.append(f'              <span class="case-seq__num" aria-hidden="true">{i}</span>')
            if "subhead" in rs:
                L.append(f'              <h3 class="case-subhead">{bl(esc(rs["subhead"]), esc(es["subhead"]))}</h3>')
            for a, b in zip(rs["paragraphs"], es["paragraphs"]):
                L.append(f'              <p>{bl(esc(a), esc(b))}</p>')
            L.append('            </div>')
            L.append('            <div class="col-8">')
            for rf, ef in zip(rs["figures"], es["figures"]):
                L.append(figure(rf, ef, 14))
            L.append('            </div>')
            L.append('          </li>')
        L.append('        </ol>')

    elif t == "compare-pair":
        # Два варианта одного интерфейса. Раньше пара жила внутри col-8-center
        # и каждый концепт получал около 356 px — интерфейс на такой ширине
        # не читался. Теперь это обычная строка сетки: по 6 колонок из 12 на
        # концепт (предел для изображения), оба остаются в одном ряду,
        # на мобильном встают друг под другом.
        L.append('        <div class="case-grid case-figs--labelled">')
        for rf, ef in zip(rb["figures"], eb["figures"]):
            L += ['          <div class="case-figs__item col-6">',
                  f'            <p class="case-figs__label">{bl(esc(rf["label"]), esc(ef["label"]))}</p>',
                  figure(rf, ef, 12),
                  '          </div>']
        L.append('        </div>')

    elif t == "theme":
        L.append('        <div class="case-grid case-split'
                 + (' case-split--flip' if rb.get("media_first") else '') + '">')
        L.append('          <div class="case-split-text col-4">')
        L += subhead(12) + paragraphs(12)
        L.append('          </div>')
        L.append('          <div class="col-8">')
        L.append(slider(rb["pair"], state["sec_title_ru"], state["sec_title_en"], 12))
        L.append('          </div>')
        L.append('        </div>')
        if "table" in rb:
            L.append(table_html(rb["table"], eb["table"], 8, narrow=True, label=(state["sec_title_ru"], state["sec_title_en"])))

    elif t == "table":
        L.append(table_html(rb, eb, 8, label=(state["sec_title_ru"], state["sec_title_en"])))

    elif t == "result-cards":
        L.append('        <div class="case-grid result-cards">')
        for rc, ec in zip(rb["cards"], eb["cards"]):
            L += ['          <div class="result-card col-6">',
                  f'            <p class="result-card__label">{bl(esc(rc["label"]), esc(ec["label"]))}</p>',
                  f'            <h3 class="result-card__metric">{bl(esc(rc["title"]), esc(ec["title"]))}</h3>',
                  f'            <p class="result-card__desc">{bl(esc(rc["text"]), esc(ec["text"]))}</p>',
                  '            <p class="result-card__measure">',
                  f'              <span class="result-card__measure-label">{bl(*MEASURE)}</span>',
                  f'              <span>{bl(esc(rc["measure"]), esc(ec["measure"]))}</span>',
                  '            </p>',
                  '          </div>']
        L.append('        </div>')

    elif t == "note-line":
        pass

    else:
        raise SystemExit(f"неизвестный тип блока: {t}")


def build(rc):
    ec = en_cases[rc["id"]]
    L = ['    <div class="case-page">', '      <div class="case-header">',
         f'        <h1 class="case-title">{esc(rc["title"])}</h1>',
         f'        <p class="case-headline">{bl(esc(rc["subtitle"]), esc(ec["subtitle"]))}</p>',
         '        <dl class="case-facts">']
    for (rk, rv), ev in zip(rc["meta"].items(), ec["meta"].values()):
        L.append(f'          <div><dt>{bl(esc(rk), esc(META_EN[rk]))}</dt><dd>{bl(esc(rv), esc(ev))}</dd></div>')
    L += ['        </dl>', '        <div class="case-grid case-context-cards">']
    for key, lru, len_ in CTX:
        r, e = rc[key], ec[key]
        L += ['          <div class="case-context-card col-6">',
              f'            <p class="case-context-card__label">{bl(lru, len_)}</p>',
              f'            <h2 class="case-context-card__title">{bl(esc(r["title"]), esc(e["title"]))}</h2>',
              f'            <p class="case-context-card__text">{bl(esc(r["text"]), esc(e["text"]))}</p>',
              '          </div>']
    L += ['        </div>', '      </div>']

    state = {"splits": 0, "case_title": rc["title"]}
    en_sec = {s["id"]: s for s in ec["sections"]}
    for rs in rc["sections"]:
        es = en_sec[rs["id"]]
        results = rs.get("kind") == "results"
        state["sec_title_ru"], state["sec_title_en"] = rs["title"], es["title"]
        # Если секция начинается сразу с двухколоночного блока, заголовок
        # уезжает в текстовую колонку: иначе он висит наверху отдельно от
        # своего же описания.
        first = rs["blocks"][0]
        in_column = (not results and first["type"] in ("split", "theme")
                     and first.get("layout") in (None, "even", "accent"))
        state["head_in_column"] = in_column
        L.append(f'\n      <div class="detail-block{" case-results" if results else ""}" id="{rs["id"]}">')
        if results:
            L.append('        <div class="case-results__panel">')
        if not in_column:
            L += ['        <div class="detail-head">',
                  f'          <h2>{bl(esc(rs["title"]), esc(es["title"]))}</h2>',
                  '        </div>']
        for rb, eb in zip(rs["blocks"], es["blocks"]):
            render_block(rb, eb, L, state)
        if results:
            L.append('        </div>')
        L.append('      </div>')

    L.append('    </div>')
    return "\n".join(L)


BLOCK = re.compile(r'    <div class="case-page">.*?\n    </div>\n(?=\s*<nav class="case-floating-nav">)', re.S)
for cid, fname in PAGES.items():
    rc = next(c for c in ru_doc["cases"] if c["id"] == cid)
    p = ROOT / fname
    t = p.read_text()
    assert len(BLOCK.findall(t)) == 1, fname
    p.write_text(BLOCK.sub(lambda m: build(rc) + "\n", t))
    print("собрана", fname)
