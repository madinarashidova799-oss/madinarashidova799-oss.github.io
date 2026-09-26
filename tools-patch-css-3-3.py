#!/usr/bin/env python3
"""Редакция 3.3: единая левая ось, мера текста в 6 колонок, кадр-кнопка.

Добавляет блок между маркерами в конец блока редакции 3.2 на четырёх
страницах кейсов и убирает правила элементов, которых больше нет в разметке
(«Открыть изображение», метки «Светлая/Тёмная», кнопки «крупно»).
Идемпотентно. Запуск из корня репозитория: python3 tools-patch-css-3-3.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ["case-alif-partners.html", "case-eaj-trader.html",
         "case-namaste.html", "case-360-tracker.html"]
END = "  /* ===== конец блока редакции 3.2 ===== */"
START = "  /* ===== Редакция 3.3: единая левая ось ====="
STOP = "  /* ===== конец блока редакции 3.3 ===== */"

BODY = START + """
     Заголовок, вводный абзац и вывод стоят на одной левой оси и не шире
     6 колонок основной сетки. Таблицы и схемы шире, но от того же края:
     сравнительные таблицы — 10 колонок, схемы — 8. Центрированных
     блоков, которые начинаются в третьей колонке, больше нет.
     Ширину 6 колонок считаем от контейнера страницы в cqi:
     (100cqi − 11 зазоров) / 2 + 5 зазоров = 50cqi − ½ зазора. */
  .case-page { container-type: inline-size; }
  .col-10 { grid-column: 1 / span 10; }
  @media (max-width: 767px) { .case-grid > .col-10 { grid-column: span 4; } }

  @media (min-width: 1100px) {
    .case-page { --measure-6: calc(50cqi - var(--grid-gutter) / 2); }
    .detail-block .detail-head h2 { max-width: var(--measure-6); }
    .detail-block > p,
    .detail-block > .case-subhead,
    .case-results__panel > p,
    .case-results__panel > .case-subhead { max-width: min(60ch, var(--measure-6)); }
  }

  /* Широкий материал под вступлением: заметный, но не оторванный отступ. */
  .case-grid.case-wide { margin-top: clamp(8px, 1vw, 16px); }
  .case-wide .case-artifact-cap:first-child { margin-top: 0; }
  .case-aside .col-8 > .case-artifact-cap:first-child { margin-top: 0; }
  .case-aside .col-8 > .compare-table-wrap:last-of-type { margin-bottom: 0; }

  /* Вывод под таблицей — в тех же 6 колонках, что и вступление.
     Первый абзац — что показало исследование, второй — решение. */
  .case-takeaway { margin-top: clamp(40px, 3.6vw, 56px); padding-left: 0; border-left: 0; }
  .detail-block .case-takeaway p { max-width: 60ch; }
  .detail-block .case-takeaway p + p { margin-top: clamp(12px, 1.2vw, 16px); }
  .case-takeaway .case-subhead { margin: 0 0 8px; }
  /* Новая часть секции после материала и вывода — отдельный абзац воздуха. */
  .detail-block > .case-grid + .case-subhead { margin-top: clamp(56px, 5vw, 80px); }
  .detail-block .case-takeaway p + .case-subhead { margin-top: clamp(28px, 2.6vw, 36px); }

  /* Короткая таблица решений в текстовой колонке рядом с визуалом. */
  .case-split-text .case-table-wrap--compact { margin: clamp(24px, 2.4vw, 32px) 0 0; max-width: none; }
  .case-table-wrap--compact .case-table { min-width: 0; }
  .case-table-wrap--compact .case-table th,
  .case-table-wrap--compact .case-table td { padding: 12px clamp(12px, 1.2vw, 16px); }
  .case-table-wrap--compact .case-table tbody th { position: static; min-width: 0; }

  /* Схема структуры на телефоне: в 335 px мелкие подписи сжимались до ~5 px.
     Схема держит 600 px и прокручивается внутри своего блока, подписи
     остаются читаемыми; нажатие по-прежнему открывает её целиком. */
  @media (max-width: 767px) {
    .case-split .case-fig--plain { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .case-split .case-fig--plain .case-shot { width: 600px; max-width: none; }
  }

  /* Кадр с интерфейсом — настоящая кнопка: мышь, касание, Enter, пробел. */
  button.case-shot {
    font: inherit; color: inherit; text-align: inherit;
    -webkit-appearance: none; appearance: none;
  }
  button.case-shot:focus-visible { outline: 2px solid var(--case-mark-text); outline-offset: 3px; }
""" + STOP + "\n"

# Правила удалённых элементов: сами селекторы и их комментарии.
DEAD = [
  r"  /\* Строка подписи высотой 22 px.*?\*/\n",
  r"  \.case-fig__open[^{\n]*\{[^}]*\}\n",
  r"  /\* Кнопки «крупно» под слайдером тем.*?\*/\n",
  r"  \.compare-slider__zooms?[^{\n]*\{[^}]*\}\n",
  r"  \.compare-slider__tag[^{\n]*\{[^}]*\}\n",
  r"  @media \(max-width: 480px\) \{\n    \.compare-slider__tag--right[^}]*\}\n  \}\n",
]

for name in PAGES:
    p = ROOT / name
    t = p.read_text()
    t = re.sub(re.escape(START) + r".*?" + re.escape(STOP) + r"\n", "", t, flags=re.S)
    for pat in DEAD:
        t = re.sub(pat, "", t, flags=re.S)
    assert t.count(END) == 1, name
    t = t.replace(END, BODY + "\n" + END)
    p.write_text(t)
    print("3.3 →", name)
