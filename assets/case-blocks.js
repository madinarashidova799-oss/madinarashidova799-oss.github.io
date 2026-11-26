/* Shared case blocks (v4): canvas (.cv), author comment (.cmw), metric tree (.mt-tree).
   Several blocks per page are supported (everything is scoped to its own root,
   no global ids). Language switching is done by assets/i18n.js; this file only
   listens to its "langchange" event to redraw connectors. */
(function () {
  'use strict';
  var doc = document;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $$(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  var NS = 'http://www.w3.org/2000/svg';

  /* element box in world coordinates, independent of the current zoom */
  function worldBox(world, el) {
    var wr = world.getBoundingClientRect(), k = wr.width / world.offsetWidth, r = el.getBoundingClientRect();
    return { x: (r.left - wr.left) / k, y: (r.top - wr.top) / k, w: r.width / k, h: r.height / k };
  }
  /* connectors: only in the gap between frames, never over a screen */
  function drawLinks(world, svg) {
    function byId(id) { return world.querySelector('[id="' + id + '"]'); }
    $$('.lkp', svg).forEach(function (n) { n.parentNode.removeChild(n); });
    $$('.cv-lk[data-k="p"]', world).forEach(function (lab) {
      var src = byId(lab.getAttribute('data-src')), sf = byId(lab.getAttribute('data-sf')), df = byId(lab.getAttribute('data-dst'));
      if (!src || !sf || !df || !sf.offsetWidth || !df.offsetWidth) return;
      var sb = worldBox(world, src), fb = worldBox(world, sf.querySelector('.cv-img')), db = worldBox(world, df.querySelector('.cv-img'));
      var x1 = fb.x + fb.w, y1 = Math.min(fb.y + fb.h - 16, Math.max(fb.y + 16, sb.y + sb.h / 2)),
          x2 = db.x, y2 = db.y + db.h / 2, xm = (fb.x + fb.w + db.x) / 2;
      lab.style.left = (x1 + 18) + 'px'; lab.style.top = y1 + 'px';
      var P = [[x1, y1], [xm, y1], [xm, y2], [x2 - 10, y2]], d = 'M' + P[0][0] + ' ' + P[0][1];
      for (var i = 1; i < P.length - 1; i++) {
        var a = P[i - 1], c = P[i], e = P[i + 1], l1 = Math.hypot(c[0] - a[0], c[1] - a[1]), l2 = Math.hypot(e[0] - c[0], e[1] - c[1]),
            r = Math.min(12, l1 / 2, l2 / 2);
        var ax = c[0] + (a[0] - c[0]) / l1 * r, ay = c[1] + (a[1] - c[1]) / l1 * r,
            bx = c[0] + (e[0] - c[0]) / l2 * r, by = c[1] + (e[1] - c[1]) / l2 * r;
        d += ' L' + ax + ' ' + ay + ' Q' + c[0] + ' ' + c[1] + ' ' + bx + ' ' + by;
      }
      d += ' L' + P[P.length - 1][0] + ' ' + P[P.length - 1][1];
      var p = doc.createElementNS(NS, 'path'); p.setAttribute('class', 'lkp pr'); p.setAttribute('d', d); svg.appendChild(p);
      var ar = doc.createElementNS(NS, 'polygon'); ar.setAttribute('class', 'lkp');
      ar.setAttribute('points', x2 + ',' + y2 + ' ' + (x2 - 12) + ',' + (y2 - 6) + ' ' + (x2 - 12) + ',' + (y2 + 6)); svg.appendChild(ar);
      var dt = doc.createElementNS(NS, 'circle'); dt.setAttribute('class', 'lkp'); dt.setAttribute('cx', x1); dt.setAttribute('cy', y1); dt.setAttribute('r', 3); svg.appendChild(dt);
    });
  }

  /* ===================== canvas ===================== */
  function initCanvas(cv) {
    var vp = cv.querySelector('.cv-vp'), world = cv.querySelector('.cv-world'),
        zl = cv.querySelector('.cv-zl'), svg = cv.querySelector('.cv-svg');
    if (!vp || !world || !svg) return;
    function byId(id) { return cv.querySelector('[id="' + id + '"]'); }
    var A = (cv.getAttribute('data-all') || '0 0 1000 1000').split(' ').map(Number),
        ALLR = { x: A[0], y: A[1], w: A[2], h: A[3] };
    var MIN = .06, MAX = 2.5, s = 1, x = 0, y = 0, raf = 0, dragged = false, touched = false;

    function apply() {
      world.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0) scale(' + s + ')';
      if (zl) zl.textContent = Math.round(s * 100) + '%';
      var g = 24 * s;
      vp.style.backgroundSize = g + 'px ' + g + 'px';
      vp.style.backgroundImage = g < 8 ? 'none' : '';
      vp.style.backgroundPosition = x + 'px ' + y + 'px';
    }
    function vr() { return vp.getBoundingClientRect(); }
    function zoomAt(cx, cy, ns) { ns = clamp(ns, MIN, MAX); x = cx - (cx - x) * ns / s; y = cy - (cy - y) * ns / s; s = ns; apply(); }
    function go(ns, nx, ny) {
      cancelAnimationFrame(raf);
      if (reduce) { s = ns; x = nx; y = ny; apply(); return; }
      var s0 = s, x0 = x, y0 = y, t0 = performance.now(), D = 480;
      (function st(t) {
        var k = Math.min(1, (t - t0) / D), e = 1 - Math.pow(1 - k, 3);
        s = s0 + (ns - s0) * e; x = x0 + (nx - x0) * e; y = y0 + (ny - y0) * e; apply();
        if (k < 1) raf = requestAnimationFrame(st);
      })(t0);
    }
    function targetFor(b, p) {
      var r = vr(), pad = p != null ? p : Math.min(40, r.width * .05),
          ns = clamp(Math.min((r.width - 2 * pad) / b.w, (r.height - 2 * pad) / b.h), MIN, MAX);
      return [ns, r.width / 2 - (b.x + b.w / 2) * ns, r.height / 2 - (b.y + b.h / 2) * ns];
    }
    function fitRect(b) { var t = targetFor(b); go(t[0], t[1], t[2]); }
    function secRect(id) {
      var el = byId(id); if (!el) return ALLR;
      return { x: el.offsetLeft, y: el.offsetTop - 56, w: el.offsetWidth, h: el.offsetHeight + 56 };
    }
    $$('.cv-lk', world).forEach(function (l) { world.appendChild(l); });
    function links() { drawLinks(world, svg); }

    /* pan and pinch */
    var ptr = new Map(), last = null;
    vp.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.cv-ctl') || e.button > 0) return;
      ptr.set(e.pointerId, { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY });
      cancelAnimationFrame(raf); dragged = false; touched = true; vp.classList.add('cv-grab');
      var hn = vp.querySelector('.cv-hint'); if (hn) hn.classList.add('gone');
      if (ptr.size === 2) {
        var v = Array.from(ptr.values());
        last = { d: Math.hypot(v[0].x - v[1].x, v[0].y - v[1].y), cx: (v[0].x + v[1].x) / 2, cy: (v[0].y + v[1].y) / 2 };
      }
    });
    vp.addEventListener('pointermove', function (e) {
      var p = ptr.get(e.pointerId); if (!p) return;
      var dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY;
      if (!dragged && Math.hypot(e.clientX - p.sx, e.clientY - p.sy) > 5) {
        dragged = true; ptr.forEach(function (_, id) { try { vp.setPointerCapture(id); } catch (er) {} });
      }
      if (ptr.size === 1) { x += dx; y += dy; apply(); }
      else if (ptr.size === 2 && last) {
        var v = Array.from(ptr.values()), d = Math.hypot(v[0].x - v[1].x, v[0].y - v[1].y),
            cx = (v[0].x + v[1].x) / 2, cy = (v[0].y + v[1].y) / 2, r = vr();
        zoomAt(cx - r.left, cy - r.top, s * d / last.d); x += cx - last.cx; y += cy - last.cy; apply();
        last = { d: d, cx: cx, cy: cy };
      }
    });
    function up(e) { ptr.delete(e.pointerId); last = null; if (!ptr.size) vp.classList.remove('cv-grab'); }
    vp.addEventListener('pointerup', up); vp.addEventListener('pointercancel', up);
    vp.addEventListener('wheel', function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault(); touched = true; cancelAnimationFrame(raf);
      var r = vr(), f = Math.exp(-e.deltaY * (e.ctrlKey ? .01 : .0016));
      zoomAt(e.clientX - r.left, e.clientY - r.top, s * f);
    }, { passive: false });

    cv.__cv = { fitSec: function (id) { touched = true; var t = cv.querySelector('.cv-tip'); if (t) t.classList.add('gone'); fitRect(secRect(id)); } };
    function step(f) { touched = true; var r = vr(); zoomAt(r.width / 2, r.height / 2, s * f); }
    var bIn = cv.querySelector('[data-cv="in"]'), bOut = cv.querySelector('[data-cv="out"]'), bFit = cv.querySelector('[data-cv="fit"]');
    if (bIn) bIn.addEventListener('click', function () { step(1.25); });
    if (bOut) bOut.addEventListener('click', function () { step(.8); });
    if (bFit) bFit.addEventListener('click', function () { touched = true; fitRect(ALLR); });
    vp.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k === '+' || k === '=') step(1.25); else if (k === '-') step(.8);
      else if (k === '0') { touched = true; fitRect(ALLR); }
      else if (k === 'ArrowLeft') { x += 60; apply(); } else if (k === 'ArrowRight') { x -= 60; apply(); }
      else if (k === 'ArrowUp') { y += 60; apply(); } else if (k === 'ArrowDown') { y -= 60; apply(); }
      else return;
      e.preventDefault();
    });

    /* frame selection with its pixel size */
    $$('.cv-fr', world).forEach(function (f) {
      var im = f.querySelector('img'), sz = f.querySelector('.cv-sz');
      function lab() { if (!sz) return; var px = f.getAttribute('data-px'); if (px) sz.textContent = px; else if (im && im.naturalWidth) sz.textContent = im.naturalWidth + ' × ' + im.naturalHeight; }
      if (im) { if (im.complete) lab(); im.addEventListener('load', function () { lab(); links(); }); }
      f.querySelector('.cv-img').addEventListener('click', function () {
        if (dragged) return;
        var on = !f.classList.contains('cv-on');
        $$('.cv-fr.cv-on', world).forEach(function (n) { n.classList.remove('cv-on'); });
        f.classList.toggle('cv-on', on);
      });
    });
    $$('[data-fit]', cv).forEach(function (h) {
      h.addEventListener('click', function () {
        if (dragged) return; touched = true;
        var t = cv.querySelector('.cv-tip'); if (t) t.classList.add('gone');
        fitRect(secRect(h.getAttribute('data-fit')));
      });
    });
    vp.addEventListener('click', function (e) {
      if (!e.target.closest('.cv-fr') && !dragged) $$('.cv-fr.cv-on', world).forEach(function (n) { n.classList.remove('cv-on'); });
    });

    /* the whole board by frame width, pinned to the top; on a phone the frame height follows the board's proportions */
    function fitNow() {
      var r = vr(); if (!r.width) return;
      var narrow = r.width < 600, pad = narrow ? 8 : 24, top = narrow ? 128 : 64, sc = clamp((r.width - 2 * pad) / ALLR.w, MIN, MAX);
      if (narrow) { var h = Math.round(ALLR.h * sc + top + 56); if (Math.abs(h - r.height) > 1) { vp.style.height = h + 'px'; r = vr(); } }
      else if (vp.style.height) { vp.style.height = ''; r = vr(); }
      s = sc; x = pad - ALLR.x * sc; y = top - ALLR.y * sc; apply();
    }
    var imgs = $$('img', world);
    Promise.all(imgs.map(function (i) { return i.complete ? 1 : new Promise(function (r) { i.onload = i.onerror = r; }); }))
      .then(function () { links(); if (!touched) fitNow(); });
    if (window.ResizeObserver) new ResizeObserver(function () { if (!touched) fitNow(); links(); }).observe(vp);
    addEventListener('resize', links);
    doc.addEventListener('langchange', function () { requestAnimationFrame(links); });
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(links);
    apply();
  }

  /* ===================== comments ===================== */
  var cws = $$('.cmw');
  function setOpen(w, open, focus) {
    var ic = w.querySelector('.cm-ic'), card = w.querySelector('.cm-card');
    card.hidden = !open; w.classList.toggle('is-open', open); ic.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (focus) (open ? card.querySelector('.cm-x') : ic).focus({ preventScroll: true });
  }
  function isOpen(w) { return !w.querySelector('.cm-card').hidden; }
  cws.forEach(function (w) {
    var ic = w.querySelector('.cm-ic'), card = w.querySelector('.cm-card');
    if (!ic || !card) return;
    ic.addEventListener('click', function () {
      var open = card.hidden;
      if (open) cws.forEach(function (o) { if (o !== w && isOpen(o)) setOpen(o, false, false); });
      setOpen(w, open, open);
    });
    w.querySelector('.cm-x').addEventListener('click', function () { setOpen(w, false, true); });
  });
  /* on narrow screens the card overlays the text, so nothing starts open */
  if (window.matchMedia && matchMedia('(max-width:1080px)').matches)
    cws.forEach(function (w) { if (w.querySelector('.cm-ic') && w.querySelector('.cm-card') && isOpen(w)) setOpen(w, false, false); });
  if (cws.length) {
    doc.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      var o = cws.filter(isOpen)[0]; if (o) setOpen(o, false, true);
    });
    doc.addEventListener('click', function (e) {
      cws.forEach(function (w) { if (isOpen(w) && !w.contains(e.target)) setOpen(w, false, false); });
    });
  }

  /* ===================== metric tree ===================== */
  function initTree(tree) {
    var svg = tree.querySelector('svg'); if (!svg) return;
    function draw() {
      svg.textContent = '';
      if (window.innerWidth <= 900) return;
      var tr = tree.getBoundingClientRect(); svg.setAttribute('viewBox', '0 0 ' + tr.width + ' ' + tr.height);
      $$('[data-p]', tree).forEach(function (n) {
        var p = tree.querySelector('[data-n="' + n.getAttribute('data-p') + '"]'); if (!p) return;
        var a = p.getBoundingClientRect(), b = n.getBoundingClientRect();
        var x1 = a.right - tr.left, y1 = a.top + a.height / 2 - tr.top, x2 = b.left - tr.left, y2 = b.top + b.height / 2 - tr.top, mx = (x1 + x2) / 2;
        var path = doc.createElementNS(NS, 'path');
        path.setAttribute('d', 'M' + x1 + ' ' + y1 + ' C ' + mx + ' ' + y1 + ', ' + mx + ' ' + y2 + ', ' + x2 + ' ' + y2);
        path.setAttribute('fill', 'none'); path.setAttribute('stroke', '#BDBDB7'); path.setAttribute('stroke-width', '1');
        svg.appendChild(path);
      });
    }
    draw(); addEventListener('resize', draw);
    if (window.ResizeObserver) new ResizeObserver(draw).observe(tree);
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(draw);
    doc.addEventListener('langchange', function () { requestAnimationFrame(draw); });
  }


  /* ===================== mini boards: a copy of chosen sections of the full board ===================== */
  var miniSeq = 0;
  function initMini(host) {
    var board = doc.getElementById(host.getAttribute('data-board')), bw = board && board.querySelector('.cv-world');
    if (!bw) return;
    var secs = (host.getAttribute('data-secs') || '').split(','), pre = 'm' + (++miniSeq) + '-', cur = secs[0];
    var world = doc.createElement('div'); world.className = 'cv-world'; world.setAttribute('aria-hidden', 'true');
    world.style.width = bw.style.width; world.style.height = bw.style.height;
    var svg = doc.createElementNS(NS, 'svg'); svg.setAttribute('class', 'cv-svg'); svg.setAttribute('aria-hidden', 'true'); world.appendChild(svg);
    function reid(root) {
      $$('[id]', root).concat(root.id ? [root] : []).forEach(function (n) { n.id = pre + n.id; });
      $$('[data-fit]', root).forEach(function (n) { n.removeAttribute('data-fit'); n.tabIndex = -1; });
    }
    secs.forEach(function (id) {
      var sc = bw.querySelector('[id="' + id + '"]'); if (!sc) return;
      var c = sc.cloneNode(true); reid(c); world.appendChild(c);
    });
    $$('.cv-lk[data-k="p"]', bw).forEach(function (lk) {
      var sf = bw.querySelector('[id="' + lk.getAttribute('data-sf') + '"]'), sc = sf && sf.closest('.cv-sect');
      if (!sc || secs.indexOf(sc.id) < 0) return;
      var c = lk.cloneNode(true);
      ['data-src', 'data-sf', 'data-dst'].forEach(function (k) { c.setAttribute(k, pre + c.getAttribute(k)); });
      world.appendChild(c);
    });
    host.appendChild(world);

    var lastW = 0;
    var multi = secs.length > 1 && !host.parentNode.querySelector('.mini-b');
    if (multi) cur = '*';
    function rectFor(id) {
      var els = id === '*' ? $$('.cv-sect', world) : [world.querySelector('[id="' + pre + id + '"]')];
      els = els.filter(Boolean); if (!els.length) return null;
      var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      els.forEach(function (el) {
        x0 = Math.min(x0, el.offsetLeft); y0 = Math.min(y0, el.offsetTop - 56);
        x1 = Math.max(x1, el.offsetLeft + el.offsetWidth); y1 = Math.max(y1, el.offsetTop + el.offsetHeight);
      });
      return { x: x0, y: y0, w: x1 - x0, h: y1 - y0, els: els };
    }
    function show(id) {
      cur = id;
      var W = host.clientWidth; if (!W) return; lastW = W;
      if (id !== '*') {
        var el = world.querySelector('[id="' + pre + id + '"]'); if (!el) return;
        $$('.cv-sect', world).forEach(function (n) { n.style.display = n === el ? '' : 'none'; });
        $$('.cv-lk', world).forEach(function (n) { var sf = world.querySelector('[id="' + n.getAttribute('data-sf') + '"]'); n.style.display = sf && el.contains(sf) ? '' : 'none'; });
      }
      var r = rectFor(id); if (!r) return;
      var pad = 16, sc = (W - 2 * pad) / r.w;
      host.style.height = Math.round(r.h * sc + 2 * pad) + 'px';
      world.style.transform = 'translate3d(' + (pad - r.x * sc) + 'px,' + (pad - r.y * sc) + 'px,0) scale(' + sc + ')';
      var g = Math.max(4, 16 * sc) + 'px'; host.style.backgroundSize = g + ' ' + g;
      drawLinks(world, svg);
    }
    var imgs = $$('img', world);
    Promise.all(imgs.map(function (i) { return i.complete ? 1 : new Promise(function (r) { i.onload = i.onerror = r; }); })).then(function () { show(cur); });
    show(cur);
    if (window.ResizeObserver) new ResizeObserver(function () { if (host.clientWidth !== lastW) show(cur); }).observe(host);
    addEventListener('resize', function () { show(cur); });
    doc.addEventListener('langchange', function () { requestAnimationFrame(function () { show(cur); }); });
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { show(cur); });

    /* enlarged view: a small Figma-like canvas, wheel or pinch to zoom, drag to pan */
    function open() {
      var r = rectFor(cur); if (!r) return;
      var en = doc.documentElement.lang === 'en';
      var ov = doc.createElement('div'); ov.className = 'cv-zoom';
      ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
      ov.setAttribute('aria-label', en ? 'Enlarged section' : 'Увеличенная секция');
      var box = doc.createElement('div'); box.className = 'cv-zoom-box';
      var w2 = world.cloneNode(true);
      $$('[id]', w2).forEach(function (n) { n.removeAttribute('id'); });
      box.appendChild(w2);
      var x = doc.createElement('button'); x.type = 'button'; x.className = 'cv-zoom-x';
      x.setAttribute('aria-label', en ? 'Close' : 'Закрыть');
      x.innerHTML = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 2l10 10M12 2 2 12"/></svg>';
      var hint = doc.createElement('span'); hint.className = 'cv-zoom-h';
      hint.textContent = en ? 'Wheel or pinch to zoom · drag to pan' : 'Колесо или щипок: масштаб · перетаскивайте: сдвиг';
      ov.appendChild(box); ov.appendChild(x); ov.appendChild(hint); doc.body.appendChild(ov);
      var pad = 24, BW = innerWidth - 48, BH = innerHeight - 48,
          fit = Math.min((BW - 2 * pad) / r.w, (BH - 2 * pad) / r.h);
      var bw = Math.min(BW, Math.round(r.w * fit + 2 * pad)), bh = Math.min(BH, Math.round(r.h * fit + 2 * pad));
      box.style.width = bw + 'px'; box.style.height = bh + 'px';
      var sc = fit, tx = (bw - r.w * fit) / 2 - r.x * fit, ty = (bh - r.h * fit) / 2 - r.y * fit;
      function draw() {
        w2.style.transform = 'translate3d(' + tx + 'px,' + ty + 'px,0) scale(' + sc + ')';
        var g = Math.max(6, 16 * sc) + 'px'; box.style.backgroundSize = g + ' ' + g;
        box.style.backgroundPosition = tx + 'px ' + ty + 'px';
      }
      draw();
      function zoomAt(cx, cy, ns) { ns = clamp(ns, fit * .6, 2.5); tx = cx - (cx - tx) * ns / sc; ty = cy - (cy - ty) * ns / sc; sc = ns; draw(); }
      box.addEventListener('wheel', function (e) {
        e.preventDefault(); var bb = box.getBoundingClientRect();
        zoomAt(e.clientX - bb.left, e.clientY - bb.top, sc * Math.exp(-e.deltaY * (e.ctrlKey ? .01 : .0025)));
      }, { passive: false });
      var ptr = new Map(), lastD = 0, moved = false;
      box.addEventListener('pointerdown', function (e) { ptr.set(e.pointerId, [e.clientX, e.clientY]); moved = false; try { box.setPointerCapture(e.pointerId); } catch (er) {} box.classList.add('grab'); });
      box.addEventListener('pointermove', function (e) {
        if (!ptr.has(e.pointerId)) return;
        var p = ptr.get(e.pointerId), dx = e.clientX - p[0], dy = e.clientY - p[1];
        if (ptr.size === 2) {
          ptr.set(e.pointerId, [e.clientX, e.clientY]);
          var v = Array.from(ptr.values()), d = Math.hypot(v[0][0] - v[1][0], v[0][1] - v[1][1]), b = box.getBoundingClientRect();
          if (lastD) zoomAt((v[0][0] + v[1][0]) / 2 - b.left, (v[0][1] + v[1][1]) / 2 - b.top, sc * d / lastD);
          lastD = d; moved = true; return;
        }
        if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
        tx += dx; ty += dy; ptr.set(e.pointerId, [e.clientX, e.clientY]); draw();
      });
      function up(e) { ptr.delete(e.pointerId); lastD = 0; if (!ptr.size) box.classList.remove('grab'); }
      box.addEventListener('pointerup', up); box.addEventListener('pointercancel', up);
      box.addEventListener('click', function (e) { e.stopPropagation(); });
      var prevOv = doc.body.style.overflow; doc.body.style.overflow = 'hidden';
      function close() { doc.removeEventListener('keydown', key); doc.body.removeChild(ov); doc.body.style.overflow = prevOv; host.focus(); }
      function key(e) {
        if (e.key === 'Escape') { e.preventDefault(); close(); }
        else if (e.key === 'Tab') { e.preventDefault(); x.focus(); }
        else if (e.key === '+' || e.key === '=') zoomAt(bw / 2, bh / 2, sc * 1.25);
        else if (e.key === '-') zoomAt(bw / 2, bh / 2, sc * .8);
      }
      ov.addEventListener('click', close); x.addEventListener('click', close); doc.addEventListener('keydown', key);
      x.focus();
    }
    host.addEventListener('click', open);
    host.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    var bar = host.parentNode.querySelector('.mini-b');
    if (bar) $$('button[data-sec]', bar).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('button', bar).forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        show(b.getAttribute('data-sec'));
      });
    });
  }

  $$('.cv').forEach(initCanvas);
  $$('.cv-mini').forEach(initMini);
  $$('.mt-tree').forEach(initTree);
})();
