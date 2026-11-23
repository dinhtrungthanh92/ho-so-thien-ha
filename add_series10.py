#!/usr/bin/env python3
"""Bổ sung Chuyên đề 10 vào site: cập nhật JSON nguồn, ảnh, search-index, sitemap.
Chạy TRƯỚC build_site.py (build sẽ ghi đè index/series/muc-luc/sitemap).
"""
import json, os, re, shutil, html, datetime, sys
from PIL import Image

SRC = '/tmp/site_rebuild_src.json'
SITE_DIR = '/Users/jason/Desktop/hosothienha-blog'
Q10 = '/Users/jason/Desktop/quyen10'
sys.path.insert(0, Q10)

from content import TITLES as T10, KY as KYA
from content2 import KY as KYB, TABLES
KY10 = {**KYA, **KYB}

arts = json.load(open(SRC, encoding='utf-8'))
assert max(r['series'] for r in arts) == 9, 'series 10 đã tồn tại?'

# ── 1) bìa chuyên đề 10 ─────────────────────────────────────
cover_dst = f'{SITE_DIR}/assets/img/series/vol10.jpg'
im = Image.open(f'{Q10}/img/bia_sach_A4.jpg').convert('RGB')
im.thumbnail((1100, 1100), Image.LANCZOS)
im.save(cover_dst, 'JPEG', quality=82, optimize=True, progressive=True)
print('cover ->', cover_dst)

# ── 2) ảnh minh họa từng kỳ ─────────────────────────────────
ky_img_dir = f'{SITE_DIR}/assets/img/ky'
os.makedirs(ky_img_dir, exist_ok=True)


def slugify(t):
    t = html.unescape(t).lower()
    rep = {'à':'a','á':'a','ả':'a','ã':'a','ạ':'a','ă':'a','â':'a','đ':'d','è':'e','é':'e','ê':'e',
           'ì':'i','í':'i','ò':'o','ó':'o','ô':'o','ơ':'o','ù':'u','ú':'u','ư':'u','ỳ':'y',
           'ả':'a','ẻ':'e','ỉ':'i','ỏ':'o','ủ':'u','ỷ':'y','ĩ':'i','ũ':'u','ơ':'o'}
    for k, v in rep.items():
        t = t.replace(k, v)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return re.sub(r'-+', '-', t)[:70].rstrip('-')


new_rows = []
for ky in range(1, 11):
    kyno = 90 + ky
    title = T10[ky]
    slug = slugify(title)
    imgs = [f'assets/img/series/vol10.jpg']
    n = 0
    blocks = KY10[ky]
    # ảnh theo đúng thứ tự mục (giống bản PDF) — chỉ lấy ảnh, chèn sau mỗi <h2>
    figs_by_sec = {}
    from imgmap import IMG_MAP
    for path, sec, cap in IMG_MAP.get(ky, []):
        figs_by_sec.setdefault(sec, []).append((path, cap))

    body = []
    sec = -1
    for b in blocks:
        if b[0] == 'h2':
            sec += 1
            body.append(f'<h2>{html.escape(b[1])}</h2>')
            for cap, hd, rows in TABLES.get(ky, {}).get(sec, []):
                th = ''.join(f'<th>{html.escape(h)}</th>' for h in hd)
                tr = ''.join('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in r) + '</tr>' for r in rows)
                body.append(f'<table><caption>{html.escape(cap)}</caption><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>')
            for path, cap in figs_by_sec.get(sec, []):
                n += 1
                base = os.path.basename(path).replace('.jpg', '')
                dst_name = f'k{kyno}_{base}.jpg'
                srcp = os.path.join(Q10, path)
                img = Image.open(srcp).convert('RGB')
                img.thumbnail((1100, 1100), Image.LANCZOS)
                img.save(f'{ky_img_dir}/{dst_name}', 'JPEG', quality=82, optimize=True, progressive=True)
                imgs.append(f'assets/img/ky/{dst_name}')
                body.append(f'<figure class="art-fig"><img src="../../../assets/img/ky/{dst_name}" '
                            f'alt="{html.escape(cap)}" loading="lazy"><figcaption>{html.escape(cap)}</figcaption></figure>')
        elif b[0] == 'p':
            body.append(f'<p>{b[1]}</p>')
        elif b[0] == 'ul':
            body.append('<ul>' + ''.join(f'<li>{i}</li>' for i in b[1]) + '</ul>')
        elif b[0] == 'bq':
            body.append(f'<blockquote><p>{b[1]}</p></blockquote>')

    # ảnh bìa kỳ (opener) đặt đầu trang
    from imgmap import OPENERS, OPENER_CAPTIONS
    op = OPENERS[ky]
    op_base = os.path.basename(op).replace('.jpg', '')
    op_dst = f'k{kyno}_opener.jpg'
    img = Image.open(os.path.join(Q10, op)).convert('RGB')
    img.thumbnail((1200, 1200), Image.LANCZOS)
    img.save(f'{ky_img_dir}/{op_dst}', 'JPEG', quality=84, optimize=True, progressive=True)
    imgs.insert(1, f'assets/img/ky/{op_dst}')

    new_rows.append({
        'slug': slug, 'series': 10, 'ky': kyno, 'title': title,
        'body': '\n'.join(body), 'imgs': imgs,
    })
    print(f'kỳ {kyno}: {len(imgs)} ảnh · {slug}')

arts.extend(new_rows)
json.dump(arts, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('json rows:', len(arts))

# ── 3) search-index.json ────────────────────────────────────
si_path = f'{SITE_DIR}/assets/search-index.json'
si = json.load(open(si_path, encoding='utf-8'))
si = [x for x in si if not x['u'].startswith('/series/s10/')]
for r in new_rows:
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', r['body']))
    txt = re.sub(r'\s+', ' ', txt).strip()
    si.append({
        'u': f"/series/s10/{r['ky']:02d}-{r['slug']}/",
        't': html.unescape(r['title']).replace('&amp;', '&'),
        's': 10, 'k': r['ky'], 'd': txt[:200],
    })
json.dump(si, open(si_path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('search index:', len(si))
