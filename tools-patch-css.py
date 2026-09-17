#!/usr/bin/env python3
"""Компонентный CSS редакции 3.1 для четырёх страниц кейсов.

Идемпотентно: блок ограничен маркерами и при повторном прогоне заменяется.
"""
import pathlib

ROOT = pathlib.Path('/Users/madinarasidova/madina-portfolio-deploy')
START_OLD = "  /* ===== Редакция 3.1: формы подачи блоков ====="
START = "  /* ===== Редакция 3.2: формы подачи блоков ====="
END = "  /* ===== конец блока редакции 3.2 ===== */"
END_OLD = "  /* ===== конец блока редакции 3.1 ===== */"

ACCENTS = {
 "case-alif-partners.html": ("#FBBF02", "#17110E", "#8A6400"),
 "case-eaj-trader.html":    ("#1B60D9", "#FFFFFF", "#1B60D9"),
 "case-namaste.html":       ("#6F64B8", "#FFFFFF", "#6F64B8"),
 "case-360-tracker.html":   ("#5955FF", "#FFFFFF", "#4B47E0"),
}

BODY = """
  /* ===== Редакция 3.2: формы подачи блоков =====
     Ни одна иллюстрация не шире 8 колонок из 12. Две композиции:
       6 / 6 — обычная: текст и экран рядом, текст по центру визуала;
       4 / 8 — редкая: группы мобильных экранов, широкие web-интерфейсы,
               схемы процесса, сравнительные таблицы;
       col-8-center — вступление в 6 колонок сверху, таблица или схема
               в 8 колонках по центру контентной области.
     .case-seq     — один сценарий по шагам, каждый шаг в той же сетке 4/8;
     .case-cols    — параллельные наблюдения: колонка с засечкой акцента;
     .case-results — итоги: тёмная полоса и четыре карточки 2×2.
     Цвет кейса живёт в трёх переменных ниже и нигде больше не дублируется. */
  :root {
    --case-mark: __MARK__;        /* метка: точка, номер шага, засечка колонки */
    --case-mark-on: __ON__;       /* текст поверх метки */
    --case-mark-text: __TEXT__;   /* тот же акцент как текст на светлом фоне */
  }

  .col-5 { grid-column: span 5; }
  .col-7 { grid-column: span 7; }
  @media (max-width: 767px) {
    .case-grid > .col-5, .case-grid > .col-7 { grid-column: span 4; }
  }

  /* Сторону визуала выбирает содержание, а не автоматическое чередование:
     основной путь — текст слева, продолжение сценария — визуал слева.
     В разметке всегда сначала текст, поэтому на мобильном порядок
     сбрасывается и текст снова идёт первым. */
  .case-split--flip > :last-child { order: -1; }
  @media (max-width: 767px) { .case-split--flip > * { order: 0; } }
  /* Выравнивание по верхнему краю: заголовок и абзац стоят рядом с верхом
     визуала, а не разъезжаются по высоте картинки. */
  .case-split { align-items: start; }
  /* Оптическая поправка: у заголовка есть выносная линия, у рамки кадра нет. */
  .case-split-text { padding-top: 6px; }
  .case-split .compare-slider__frame { margin-top: 0; margin-bottom: 0; }

  /* ---- Текстовая колонка ----
     Заголовок и описание — один модуль: 24–32 px между ними, длина строки
     45–70 знаков, высота колонки по содержимому, без растяжки под картинку. */
  .case-split-text { align-self: start; }
  .case-lead-title {
    font-family: var(--display); font-size: var(--font-size-h2);
    line-height: var(--line-height-heading); font-weight: 700; letter-spacing: -0.01em;
    color: var(--text-strong); text-wrap: balance; max-width: 18ch;
    margin: 0 0 clamp(24px, 2.2vw, 32px);
  }
  .case-split-text .case-subhead { max-width: 22ch; margin-bottom: clamp(20px, 1.8vw, 26px); }
  .detail-block .case-split-text p { max-width: 56ch; margin-bottom: clamp(16px, 1.4vw, 20px); }
  .detail-block .case-split-text p:last-child { margin-bottom: 0; }
  .col-6.case-split-text, .col-4.case-split-text { max-width: 560px; }

  /* Высокий кадр рядом с коротким абзацем оставлял от 240 до 720 px пустой
     колонки — замерено во всех четырёх кейсах. Растягивать текст незачем,
     увеличивать картинку нельзя, поэтому текст едет вместе с кадром: он
     остаётся на экране, пока читатель проходит изображение, и подпись
     работает как комментарий к тому, что видно прямо сейчас.
     Отступ сверху уводит колонку из-под верхней навигации.
     Ниже 900 px колонки складываются в одну и липкость выключается. */
  @media (min-width: 900px) {
    .case-split > .case-split-text { position: sticky; top: clamp(96px, 12vh, 132px); }
  }

  /* Два-три коротких вывода под абзацем: та же колонка, ближе к тексту,
     чем к следующей секции. */
  .case-points {
    list-style: none; margin: clamp(32px, 3vw, 40px) 0 0; padding: 0;
    display: flex; flex-direction: column; gap: clamp(18px, 1.8vw, 24px);
  }
  .case-points li { position: relative; padding-top: 16px; border-top: 1px solid var(--line-strong); }
  .case-points li::before {
    content: ''; position: absolute; top: -1px; left: 0; width: 36px; height: 2px;
    background: var(--case-mark);
  }
  .detail-block .case-points__title {
    font-family: var(--display); font-weight: 600; font-size: var(--font-size-label);
    line-height: 1.4; color: var(--text); margin: 0 0 4px; max-width: none;
  }
  .detail-block .case-points__text {
    font-size: 13px; line-height: 1.55; color: var(--text-dim); margin: 0; max-width: none;
  }

  .case-subhead {
    font-family: var(--display); font-weight: var(--font-weight-heading);
    font-size: var(--font-size-h3); line-height: 1.3; color: var(--text);
    margin: 0 0 12px; text-wrap: balance;
  }

  /* Вступление перед таблицей или схемой: занимает 6 колонок сетки. */
  .case-lede { max-width: 56ch; margin-bottom: clamp(24px, 2.4vw, 32px); }
  .case-lede > p:last-child { margin-bottom: 0; }
  .case-grid > .case-split-text.col-6 { margin-bottom: clamp(24px, 2.4vw, 32px); }
  .detail-head + .case-grid .case-split-text p { margin-top: 0; }
  .case-grid > .col-8-center + .col-8-center { margin-top: clamp(24px, 2.4vw, 32px); }

  /* ---- Кадр с интерфейсом ----
     Подпись вынесена из белого контейнера: раньше она входила в карточку и
     добавляла ей высоты. Внутренние поля кадра сокращены, чтобы размер
     задавал интерфейс, а не рамка вокруг него. */
  /* Кадр всегда живёт внутри своей колонки сетки: собственной ширины у него
     нет, режим «во всю страницу» убран. */
  .case-fig { max-width: none; margin: 0; min-width: 0; }
  /* Схема уже нарисована на собственной подложке — вторая рамка вокруг неё
     читалась бы как вложенная карточка. */
  .detail-block .case-fig--plain .case-shot { background: none; border: 0; padding: 0; }
  .detail-block .case-fig--plain .case-shot img { border-radius: var(--radius-large); }
  .detail-block .case-shot {
    display: block; width: 100%; max-width: none; margin: 0;
    background: var(--surface); border: 1px solid var(--line);
    border-radius: var(--radius-large);
    padding: clamp(12px, 1.2vw, 18px);
    cursor: zoom-in; transition: border-color 0.2s ease;
  }
  .detail-block .case-shot:hover { transform: none; box-shadow: none; border-color: var(--line-strong); }
  .detail-block .case-shot img {
    display: block; width: 100%; height: auto; margin: 0;
    border-radius: var(--radius-medium);
  }
  .case-fig__cap {
    display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px;
    margin: 18px 0 0;
    font-size: 13px; line-height: 1.5; color: var(--text-dim);
  }
  .case-fig__text { max-width: 62ch; }
  .case-fig__open {
    font: inherit; font-size: 12px; color: var(--case-mark-text);
    background: none; border: 0; padding: 2px 0; cursor: pointer;
    text-decoration: underline; text-underline-offset: 3px; white-space: nowrap;
  }
  .case-fig__open:hover { text-decoration-thickness: 2px; }
  /* Строка подписи высотой 22 px — слишком мелкая цель для пальца. Сама
     строка остаётся прежней, растёт только область нажатия: 44 px по
     вертикали. Подпись лежит в той же flex-строке слева, перекрытия нет. */
  .case-fig__open { position: relative; }
  .case-fig__open::after { content: ''; position: absolute; inset: -11px -6px; }
  .case-fig__open:focus-visible { outline: 2px solid var(--case-mark-text); outline-offset: 3px; border-radius: 4px; }

  /* Два экрана одного сценария — друг под другом внутри своей колонки. */
  .case-figs--stack { display: flex; flex-direction: column; gap: clamp(20px, 2.2vw, 28px); }

  /* Подписи к частям одной композиции. */
  .case-shot-labels {
    list-style: none; display: grid; grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr));
    gap: clamp(16px, 2vw, 28px); margin: clamp(20px, 2vw, 26px) 0 0; padding: 0;
  }
  .case-shot-labels li {
    font-family: var(--mono); font-size: 12px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--text-dim);
    padding-top: 10px; border-top: 1px solid var(--line-strong); position: relative;
  }
  .case-shot-labels li::before {
    content: ''; position: absolute; top: -1px; left: 0; width: 36px; height: 2px;
    background: var(--case-mark);
  }
  @media (max-width: 640px) { .case-shot-labels { grid-template-columns: 1fr; gap: 12px; } }

  /* Один сценарий по шагам. <ol>: порядок действий — часть содержания. */
  .case-seq { list-style: none; display: flex; flex-direction: column; gap: clamp(44px, 4.5vw, 72px); }
  .case-seq__step { min-width: 0; }
  .case-seq__head { position: relative; padding-left: 52px; }
  .case-seq__num {
    position: absolute; top: 1px; left: 0; width: 34px; height: 34px; border-radius: 50%;
    background: var(--case-mark); color: var(--case-mark-on);
    display: grid; place-items: center;
    font-family: var(--mono); font-size: 13px; font-weight: 500; line-height: 1;
    font-variant-numeric: tabular-nums;
  }
  .case-seq__head .case-subhead { margin-bottom: 10px; }
  .case-seq__head > p:last-child { margin-bottom: 0; }
  @media (max-width: 767px) { .case-seq__head { margin-bottom: 20px; } }
  @media (max-width: 560px) { .case-seq__head { padding-left: 46px; } }

  /* Нумерованная последовательность шагов исследования. */
  .case-rail { list-style: none; }
  .case-rail__num { background: var(--case-mark); color: var(--case-mark-on); }
  .case-rail__title { font-size: var(--font-size-h4); }
  .case-rail .case-rail__text { margin: 0; }

  /* Параллельные наблюдения: не карточки, а колонки под общей линией с
     короткой засечкой акцента. Карточка обещала бы отдельный объект. */
  .case-cols {
    display: grid; grid-template-columns: repeat(var(--cols, 2), minmax(0, 1fr));
    gap: clamp(24px, 2.6vw, 36px) clamp(24px, 2.6vw, 40px);
    margin: clamp(32px, 3.2vw, 44px) 0;
  }
  .case-col {
    position: relative; min-width: 0;
    padding-top: clamp(18px, 1.8vw, 22px); border-top: 1px solid var(--line-strong);
  }
  .case-col::before {
    content: ''; position: absolute; top: -1px; left: 0; width: 48px; height: 2px;
    background: var(--case-mark);
  }
  .case-col .case-col__label {
    font-family: var(--mono); font-size: 12px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--case-mark-text); margin: 0 0 8px; max-width: none;
  }
  .case-col__title {
    font-family: var(--display); font-weight: var(--font-weight-heading);
    font-size: var(--font-size-h4); line-height: 1.3; color: var(--text);
    margin: 0 0 8px; text-wrap: balance;
  }
  .case-col .case-col__text {
    font-size: var(--font-size-body); line-height: var(--line-height-body);
    color: var(--text-dim); margin: 0; max-width: 44ch; text-wrap: pretty;
  }
  /* Компактный вариант: три колонки читаются как подводка к решению ниже. */
  .case-cols--compact { margin-bottom: clamp(24px, 2.4vw, 32px); }
  .case-cols--compact .case-col__title { font-size: var(--font-size-h3); }
  .case-cols--compact .case-col__text { font-size: var(--font-size-label); line-height: 1.55; }
  @media (max-width: 860px) {
    .case-cols { grid-template-columns: 1fr; gap: 26px; }
    .case-col .case-col__text { max-width: none; }
  }

  /* Вывод из исследования. Отдельная реплика после материала, не ещё один абзац. */
  .case-takeaway {
    margin: clamp(28px, 2.8vw, 40px) 0 0; padding-left: clamp(18px, 2vw, 26px);
    border-left: 2px solid var(--case-mark);
  }
  .detail-block .case-takeaway p {
    margin: 0; max-width: 66ch;
    font-size: var(--font-size-body); line-height: var(--line-height-body); color: var(--text);
  }

  /* Пара концептов: у каждой картинки своя подпись-заголовок. */
  /* Пара концептов — обычная строка сетки, по 6 колонок на концепт.
     Собственная сетка .case-figs здесь не нужна, отступы задаёт .case-grid;
     на мобильном каждый концепт занимает всю ширину, отсюда row-gap. */
  .case-grid.case-figs--labelled { align-items: start; margin: clamp(32px, 3vw, 40px) 0; row-gap: clamp(24px, 2.6vw, 32px); }
  .case-figs--labelled { align-items: start; }
  .case-figs__item { min-width: 0; }
  .case-figs__item .case-figs__label {
    font-family: var(--mono); font-size: 12px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--case-mark-text); margin: 0 0 12px; max-width: none;
  }
  .detail-block p.case-artifact-cap {
    font-size: var(--font-size-label); line-height: 1.5; color: var(--text-dim);
    margin: clamp(24px, 2.4vw, 32px) 0 12px; max-width: 62ch;
  }
  .case-table-wrap--narrow { max-width: 720px; }

  /* ---- Итоги ----
     Тёмная полоса во всю ширину экрана, контент остаётся в основном
     контейнере. Полоса нарисована box-shadow + clip-path: это не влияет на
     раскладку и не создаёт горизонтальной прокрутки, в отличие от 100vw. */
  :root {
    --results-bg: #211B18;
    --results-card: #2C2723;
    --results-line: rgba(255, 255, 255, 0.11);
    --results-text: rgba(255, 255, 255, 0.68);
    --results-dim: rgba(255, 255, 255, 0.5);
  }
  .detail-block.case-results { margin-top: clamp(96px, 9vw, 140px); padding-top: 0; }
  .case-results__panel {
    position: relative; background: var(--results-bg);
    box-shadow: 0 0 0 100vmax var(--results-bg);
    clip-path: inset(0 -100vmax);
    padding: clamp(40px, 4.5vw, 72px) 0 clamp(44px, 5vw, 80px);
  }
  .case-results__panel .detail-head { margin-bottom: clamp(16px, 1.6vw, 20px); }
  .case-results__panel .detail-head h2 { color: #fff; }
  .case-results__panel p { color: var(--results-text); max-width: 62ch; }
  .case-results__panel .case-lede { margin-bottom: 0; }
  .case-results .result-cards { margin-top: clamp(28px, 3vw, 40px); row-gap: clamp(20px, 2vw, 28px); }
  .case-results .result-card {
    background: var(--results-card); border: 1px solid var(--results-line);
    border-radius: var(--radius-medium); box-shadow: none;
    min-height: 0; height: 100%;
    padding: clamp(28px, 2.6vw, 40px); gap: 10px;
  }
  .case-results .result-card .result-card__label {
    color: var(--results-dim); margin: 0 0 2px;
  }
  .case-results .result-card .result-card__label::before { background: var(--case-mark); }
  .case-results .result-card .result-card__metric {
    font-size: clamp(18px, 1.5vw, 22px); line-height: 1.3; color: #fff;
  }
  .case-results .result-card .result-card__desc { color: var(--results-text); }
  .case-results .result-card .result-card__measure {
    width: 100%; margin: auto 0 0; padding-top: 18px;
    border-top: 1px solid var(--results-line);
    font-size: 13px; line-height: 1.5; color: var(--results-text); max-width: none;
    display: flex; flex-direction: column; gap: 4px;
  }
  .case-results .result-card .result-card__measure-label {
    font-family: var(--mono); font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: var(--results-dim);
  }

  /* Ритм страницы: воздух разделяет разные истории, а не связанные части
     одной. Между самостоятельными секциями 128–176 px. */
  .detail-block { margin-top: clamp(128px, 11vw, 176px); padding-top: 0; }
  @media (max-width: 720px) { .detail-block { margin-top: clamp(88px, 14vw, 112px); } }
  .detail-block .detail-head { margin-bottom: clamp(24px, 2.2vw, 32px); }
  .detail-block:last-child .detail-head { margin-bottom: clamp(24px, 2.2vw, 32px); }

  /* Экспорты обрезаны по содержимому, пропорция набора изменилась. */
  .compare-slider__stage { aspect-ratio: 2700 / 1768; }
__SLIDER__  /* ===== конец блока редакции 3.2 ===== */
"""

SLIDER = """
  /* Кнопки «крупно» под слайдером тем: сам слайдер показывает сравнение,
     а рассмотреть экран целиком можно в лайтбоксе. */
  .compare-slider__frame { padding: clamp(12px, 1.2vw, 18px); }
  .compare-slider__tools {
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
    gap: 12px; margin-top: 12px;
  }
  .compare-slider__hint { font-size: 13px; line-height: 1.45; color: var(--text-dim-2); }
  .compare-slider__zooms { display: flex; gap: 8px; flex-wrap: wrap; }
  .compare-slider__zoom {
    font: inherit; font-size: 13px; cursor: pointer;
    background: var(--bg); border: 1px solid var(--line-strong); color: var(--text);
    border-radius: var(--radius-pill); padding: 9px 16px; min-height: 44px;
  }
  .compare-slider__zoom:hover { border-color: var(--case-mark); }
  .compare-slider__zoom:focus-visible { outline: 2px solid var(--case-mark-text); outline-offset: 2px; }

"""


def main():
    for fname, (mark, on, text) in ACCENTS.items():
        p = ROOT / fname
        t = p.read_text()
        block = (BODY.replace("__MARK__", mark).replace("__ON__", on)
                 .replace("__TEXT__", text)
                 .replace("__SLIDER__", SLIDER if fname == "case-namaste.html" else ""))
        marker = START if START in t else (START_OLD if START_OLD in t else None)
        end = END if END in t else END_OLD
        if marker:
            i = t.index(marker)
            j = t.index(end, i) + len(end)
            t = t[:i] + block.lstrip("\n").rstrip("\n") + t[j:]
        else:
            k = t.rindex("</style>")
            t = t[:k] + block + t[k:]
        p.write_text(t)
        print("patched", fname)


main()
