"""Assemble the public site into _site/ for GitHub Pages.

Only pages, the files they reference and a few root files are published.
Working notes, scripts, docs and source originals stay in the repository
but never reach the public site.
"""
import os
import shutil
import urllib.parse

OUT = '_site'
SKIP_PAGES = {'tracker_tables.html'}
ROOT_FILES = ['CNAME', '.nojekyll', 'favicon.png', 'cv.pdf', 'cv-en.pdf', 'robots.txt', 'sitemap.xml', '404.html']


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    pages = sorted(f for f in os.listdir('.') if f.endswith('.html') and f not in SKIP_PAGES)
    code = []
    for root, _, names in os.walk('assets'):
        if root.startswith(os.path.join('assets', 'source-originals')):
            continue
        for n in names:
            if n.endswith(('.js', '.css')):
                code.append(os.path.join(root, n))

    corpus = ''
    for f in pages + code:
        with open(f, encoding='utf-8') as fh:
            corpus += fh.read()

    def keep(path):
        if path in code:
            return True
        base = os.path.basename(path)
        rel = path.replace(os.sep, '/')
        return rel in corpus or base in corpus or urllib.parse.quote(rel) in corpus

    copied = 0
    for root, _, names in os.walk('assets'):
        if root.startswith(os.path.join('assets', 'source-originals')):
            continue
        for n in names:
            if n == '.DS_Store':
                continue
            src = os.path.join(root, n)
            if keep(src):
                dst = os.path.join(OUT, src)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1

    for f in pages + [r for r in ROOT_FILES if os.path.exists(r)]:
        shutil.copy2(f, os.path.join(OUT, f))

    print('pages', len(pages), 'assets', copied)


if __name__ == '__main__':
    main()
