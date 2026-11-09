---
target: case-sber-split.html
total_score: 19
max_score: 32
na_heuristics: 7,10
p0_count: 2
p1_count: 2
target_identity: "file:/Users/madinarasidova/madina-portfolio-deploy/.claude/worktrees/portfolio-product-designer-0daf18/case-sber-split.html"
target_fingerprint: "sha256:4f5ae7b39997f97bba800e31bab3154861f4a1e59acf7f0e4989a290348681cf"
target_path: /Users/madinarasidova/madina-portfolio-deploy/.claude/worktrees/portfolio-product-designer-0daf18/case-sber-split.html
timestamp: 2026-11-07T15-42-58Z
slug: case-sber-split-html
---
# Critique: case-sber-split.html (2026-11-07)
Method: dual-agent (A: design review · B: detector)
Score 19/32 (59%, Acceptable). n/a: 7, 10.
Heuristics: 1=3, 2=3, 3=2, 4=2, 5=3, 6=2, 8=1, 9=3.
## Priority issues
- [P0] Reads as a test assignment (badge, Format cell, meta, "в рамках тестового"). Fix: remove, open with the problem. clarify
- [P0] 12 sections / 24 viewports (target 7-9). Cut hypothesis, UI-kit grid, merge research+competitors, control+recipient, compress creator flow. distill
- [P1] Colour/effect overload: 4 hue ramps, 49 backdrop blurs, 14 gradients, drifting blobs, dark section. One green accent, flat white cards, participant colours only inside product UI. quieter
- [P1] Header: 2-screen sticky hero, badge, 6-cell facts, floating chips. Compact Serafima-style facts table + short role paragraph + one calm cover. layout
- [P2] Artifacts: blank/illegible thumbnails, creator flow 3.8 screens, hover-only metric tree. Bento artifact cards (visual on top, title + one line below), screens in a row. layout
- [P2] Floating case pill and sticky demo bar overlap content. polish
- [P3] Reveal-on-scroll leaves blank screens; numbering skips (01-04, 06, 09, 11); jargon (Malachite, North Star). polish/typeset
## Detector
60 CLI findings: gpt-thin-border-wide-shadow x24, cramped-padding x14, low-contrast x7 (white on #21A038 3.4:1, #2F8CFF 3.3:1, #EF3B3B 3.9:1), icon-tile-stack x5, nested-cards x3, tight-leading x2, side-tab, dark-glow, radial-halo, broken-image, overused-font. Browser: h1 span overflow 17px, numbered-section-labels x7.
