#!/usr/bin/env python3
"""Build static blog hosothienha.com from /tmp/site_content4.json (80 kỳ, 9 series)."""
import json, os, re, html, shutil, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://hosothienha.com'
arts = json.load(open('/tmp/site_rebuild_src.json'))
arts.sort(key=lambda r: r['ky'])
import re as _re, html as _html
for _r in arts:
    _t = _html.unescape(_re.sub(r'<[^>]+>', ' ', _r['body']))
    _t = _re.sub(r'\s+', ' ', _t).strip()
    _r['nwords'] = len(_t.split())
    _r['lead'] = _r.get('lead') or (_t[:260].rsplit(' ', 1)[0] + '…')
    _r.setdefault('cover', _r['imgs'][0] if _r['imgs'] else 'assets/img/series/vol%d.jpg' % _r['series'])
    _r.setdefault('nfig', max(0, len(_r['imgs']) - 1))

by_ky = {r['ky']: r for r in arts}

SERIES = {
 1: ('Tiền Sử Thiên Hà', 'Khởi nguyên Vũ trụ, Lăng Kính Lyra, các Đấng Sáng Lập và cuộc Đại Di Cư vĩ đại.'),
 2: ('Hành Trình Thiên Hà', 'Các nền văn minh thiên hà, Orion, Atlantis — Lemuria và cuộc chiến di truyền.'),
 3: ('Dòng Máu Anunnaki', 'Nibiru, Enki — Enlil, di sản 12 chuỗi DNA và ma trận tần số 3D.'),
 4: ('Văn Minh Lòng Đất', 'Trái Đất rỗng, Agartha, Telos, Shambhala và mạng lưới căn cứ ngầm.'),
 5: ('Chương Trình Không Gian Bí Mật', 'SSP, Solar Warden, ICC, Looking Glass và cuộc giải phóng Hệ Mặt Trời.'),
 6: ('Hòm Không Gian Cổ Đại', 'Space Arks dưới đáy đại dương, Nam Cực, Mặt Trăng và Sao Hỏa.'),
 7: ('Hồ Sơ Các Chủng Tộc', 'Lyra, Pleiades, Arcturus, Sirius, Draco, Greys và Hoàng gia Anunnaki.'),
 8: ('Khoa Học & Công Nghệ', 'Stargates, động cơ warp, med-beds, zero-point energy, vũ khí tần số.'),
 9: ('Cẩm Nang Tâm Thức Vũ Trụ', 'Tuyến tùng, luân xa, sóng não, DNA 12 sợi, thể vía và tần số 5D.'),
}
S_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for s in S_ORDER:
    assert [r for r in arts if r['series'] == s], f'series {s} empty'

def strip(t):
    t = html.unescape(re.sub(r'<[^>]+>', '', t))
    return re.sub(r'\s+', ' ', t).strip()

def esc(t): return html.escape(strip(t), quote=True)

def rel(root):
    return root  # every page sits at site root depth via <base>

NAV = [
    ('/', 'Trang chủ'),
    ('/series/', 'Chuyên đề'),
    ('/muc-luc/', 'Mục lục'),
    ('/gioi-thieu/', 'Giới thiệu'),
]

def layout(title, desc, body, depth=0, canonical='/', extra_head=''):
    desc = desc.replace('80 kỳ', f'{len(arts)} kỳ')
    title = title.replace('80 kỳ', f'{len(arts)} kỳ')
    r = '../' * depth
    nav = ''.join(f'<a href="{r}{h.lstrip("/")}">{n}</a>' if h != '/' else f'<a href="{r or "./"}">{n}</a>'
                  for h, n in NAV)
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:site_name" content="Hồ Sơ Thiên Hà">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="{r}assets/style.css">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
{extra_head}
</head>
<body>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{r}"><span class="mark">✦</span> Hồ Sơ Thiên Hà</a>
    <nav class="nav">{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <p><strong>Hồ Sơ Thiên Hà</strong> — thư viện chuyên đề miễn phí về lịch sử thiên hà, di sản di truyền và tâm thức vũ trụ.</p>
    <p class="fine">9 chuyên đề · {len(arts)} kỳ · nội dung biên soạn và tổng hợp. Toàn bộ nội dung được chia sẻ miễn phí cho mục đích nghiên cứu và mở rộng nhận thức.</p>
  </div>
</footer>
</body>
</html>'''

def card(r, r_=''):
    return f'''<a class="card" href="{r_}ky/{r['slug']}/">
  <span class="chip">Kỳ {r['ky']}</span>
  <h3>{esc(r['title'])}</h3>
  <p>{esc(r['lead'])}</p>
  <span class="more">Đọc →</span>
</a>'''

def write(path, content):
    p = os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)

shutil.rmtree(os.path.join(OUT, 'ky'), ignore_errors=True)
shutil.rmtree(os.path.join(OUT, 'series'), ignore_errors=True)

# ── home ──────────────────────────────────────────────────────
stats = f'''<div class="stats">
  <li><b>{len(arts)}</b><span>Kỳ</span></li>
  <li><b>9</b><span>Chuyên đề</span></li>
  <li><b>{sum(r['nwords'] for r in arts)//1000}k</b><span>Từ</span></li>
  <li><b>{sum(len(r['imgs']) for r in arts)}</b><span>Ảnh minh họa</span></li>
</div>'''

def sercards_at(prefix=''):
    return ''.join(f'''<a class="scard" href="{prefix}series/s{s}/">
  <img src="{prefix}assets/img/series/vol{s}.jpg" alt="Chuyên đề {s}: {esc(SERIES[s][0])}" loading="lazy">
  <div><span class="chip">Chuyên đề {s}</span>
  <h3>{esc(SERIES[s][0])}</h3>
  <p>{esc(SERIES[s][1])}</p>
  <span class="more">{len([r for r in arts if r['series']==s])} kỳ →</span></div>
</a>''' for s in S_ORDER)

latest = sorted(arts, key=lambda r: -r['ky'])[:9]
home = f'''<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Thư viện chuyên đề miễn phí</p>
        <h1>Hồ Sơ Thiên Hà</h1>
        <p class="lede">Từ Lăng Kính Lyra và các Đấng Sáng Lập, tới dòng máu Anunnaki, những nền văn minh lòng đất, chương trình không gian bí mật, hòm không gian cổ đại, hồ sơ các chủng tộc — và cuối cùng là cẩm nang tâm thức vũ trụ. 9 chuyên đề, {len(arts)} kỳ, đọc theo đúng mạch.</p>
        <p class="actions"><a class="btn" href="muc-luc/">Xem mục lục {len(arts)} kỳ</a><a class="btn ghost" href="series/">Khám phá chuyên đề</a></p>
      </div>
      <figure class="hero-cover"><img src="assets/img/cover-full.jpg" alt="Bìa Hồ Sơ Thiên Hà — toàn tập 9 chuyên đề" fetchpriority="high"></figure>
    </div>
    <ul class="stats-wrap">{stats}</ul>
  </div>
</section>
<section class="block wrap">
  <h2 class="sec">9 chuyên đề</h2>
  <p class="sub">Mỗi chuyên đề là một tuyến truyện liền mạch. Đọc từ kỳ đầu tới kỳ cuối, hoặc nhảy vào bất kỳ chủ đề nào bạn quan tâm.</p>
  <div class="sgrid">{sercards_at()}</div>
</section>
<section class="block wrap">
  <h2 class="sec">Kỳ mới cập nhật</h2>
  <p class="sub">Ấn phẩm mới nhất trong thư viện — kéo xuống để đọc, không cần đăng ký.</p>
  <div class="grid">{''.join(card(r) for r in latest)}</div>
  <p class="center"><a class="btn ghost" href="muc-luc/">Toàn bộ {len(arts)} kỳ →</a></p>
</section>'''
write('index.html', layout('Hồ Sơ Thiên Hà — Thư viện chuyên đề lịch sử thiên hà & tâm thức vũ trụ',
    f'{len(arts)} kỳ trong 9 chuyên đề: lịch sử thiên hà, dòng máu Anunnaki, văn minh lòng đất, chương trình không gian, hòm không gian cổ đại, hồ sơ chủng tộc, khoa học công nghệ và cẩm nang tâm thức.', home))

# ── series index + pages ─────────────────────────────────────
sbody = '<div class="wrap block"><h1 class="page">Chuyên đề</h1><p class="sub">9 tuyến truyện, ' + str(len(arts)) + ' kỳ. Bấm vào một chuyên đề để xem danh sách kỳ.</p><div class="sgrid">' + sercards_at('../') + '</div></div>'
write('series/index.html', layout('Chuyên đề — Hồ Sơ Thiên Hà', '9 chuyên đề về lịch sử thiên hà, di sản di truyền và tâm thức vũ trụ.', sbody, depth=1, canonical='/series/'))

for s in S_ORDER:
    rows = [r for r in arts if r['series'] == s]
    name, sub = SERIES[s]
    prev_s = S_ORDER[S_ORDER.index(s) - 1] if S_ORDER.index(s) > 0 else None
    next_s = S_ORDER[S_ORDER.index(s) + 1] if S_ORDER.index(s) < len(S_ORDER) - 1 else None
    kylist = ''.join(f'''<li><a href="../ky/{r['slug']}/">
      <span class="chip">Kỳ {r['ky']}</span>
      <h3>{esc(r['title'])}</h3>
      <p>{esc(r['lead'])}</p>
      <span class="more">Đọc kỳ này →</span></a></li>''' for r in rows)
    navx = ''
    if prev_s: navx += f'<a class="btn ghost" href="../series/s{prev_s}/">← Chuyên đề {prev_s}: {esc(SERIES[prev_s][0])}</a> '
    if next_s: navx += f'<a class="btn ghost" href="../series/s{next_s}/">Chuyên đề {next_s}: {esc(SERIES[next_s][0])} →</a>'
    body = f'''<div class="wrap block">
  <p class="crumb"><a href="../">Trang chủ</a> / <a href="../series/">Chuyên đề</a> / Chuyên đề {s}</p>
  <header class="series-hero">
    <img src="../../assets/img/series/vol{s}.jpg" alt="Chuyên đề {s}">
    <div>
      <p class="eyebrow">Chuyên đề {s} · {len(rows)} kỳ</p>
      <h1 class="page">{esc(name)}</h1>
      <p class="lead">{esc(sub)}</p>
    </div>
  </header>
  <ol class="kylist">{kylist}</ol>
  <p class="center pager">{navx}</p>
</div>'''
    write(f'series/s{s}/index.html', layout(f'Chuyên đề {s}: {name} — Hồ Sơ Thiên Hà', sub, body, depth=1, canonical=f'/series/s{s}/'))

# ── article pages ────────────────────────────────────────────
for r in arts:
    s = r['series']
    name = SERIES[s][0]
    rows = [x for x in arts if x['series'] == s]
    idx = [x['ky'] for x in rows].index(r['ky'])
    prev_a = rows[idx - 1] if idx > 0 else (by_ky.get(min(by_ky), None) if r['ky'] > 1 else None)
    next_a = rows[idx + 1] if idx < len(rows) - 1 else None
    if prev_a is None and r['ky'] > 1: prev_a = by_ky[r['ky'] - 1]
    if next_a is None and r['ky'] < len(arts): next_a = by_ky[r['ky'] + 1]

    imgs = r['imgs']
    # opener cover image (first) + distribute the rest evenly between <h2> sections
    cover = f'<figure class="art-fig"><img src="../../{imgs[0]}" alt="{esc(r["title"])}" loading="lazy"></figure>' if imgs else ''
    figs_head = cover
    rest = imgs[1:]
    body_html = r['body']
    gallery = ''
    if rest:
        parts = re.split(r'(<h2>)', body_html)
        # reindex: blocks of h2
        blocks, cur = [], parts[0]
        i = 1
        while i < len(parts) - 1:
            blocks.append(cur); cur = parts[i] + parts[i + 1]; i += 2
        blocks.append(cur)
        if len(blocks) <= 1:
            fig = ''.join(f'<figure class="art-fig"><img src="../../{i}" alt="{esc(r["title"])} — minh họa {n}" loading="lazy"></figure>' for n, i in enumerate(rest, 2))
            body_html = body_html + fig
        else:
            per = max(1, len(rest) // (len(blocks) - 1)) if len(blocks) > 1 else 1
            out, k = [blocks[0]], 0
            for bi, blk in enumerate(blocks[1:], 1):
                take = rest[k:k + per] if bi < len(rest) + 1 else []
                k += len(take)
                out.append(blk)
                for n, src in enumerate(take, 1):
                    out.append(f'<figure class="art-fig"><img src="../../{src}" alt="{esc(r["title"])}" loading="lazy"></figure>')
            leftover = rest[k:]
            if leftover:
                out.append('<div class="gwrap">' + ''.join(
                    f'<figure><img src="../../{src}" alt="{esc(r["title"])}" loading="lazy"></figure>' for src in leftover) + '</div>')
            body_html = ''.join(out)
    pager = '<div class="pager">'
    if prev_a: pager += f'<a class="pbtn" href="../../ky/{prev_a["slug"]}/"><small>Kỳ trước</small><b>Kỳ {prev_a["ky"]} — {esc(prev_a["title"])[:70]}</b></a>'
    if next_a: pager += f'<a class="pbtn next" href="../../ky/{next_a["slug"]}/"><small>Kỳ tiếp</small><b>Kỳ {next_a["ky"]} — {esc(next_a["title"])[:70]}</b></a>'
    pager += '</div>'

    body = f'''<div class="wrap article">
  <p class="crumb"><a href="../../">Trang chủ</a> / <a href="../../series/s{s}/">Chuyên đề {s}: {esc(name)}</a> / Kỳ {r['ky']}</p>
  <header class="art-head">
    <p class="eyebrow">Chuyên đề {s} · Kỳ {r['ky']} / {len(arts)}</p>
    <h1>{esc(r['title'])}</h1>
    <p class="meta">{r['nwords']:,} từ · {len(imgs)} hình</p>
  </header>
  {figs_head}
  <div class="prose">
{body_html}
  </div>
  {pager}
  <p class="center"><a class="btn ghost" href="../../muc-luc/">Toàn bộ mục lục</a></p>
</div>'''
    write(f'ky/{r["slug"]}/index.html', layout(
        f'Kỳ {r["ky"]}: {strip(r["title"])} — {name}', strip(r['lead']), body, depth=2,
        canonical=f'/ky/{r["slug"]}/',
        extra_head=f'<meta property="og:image" content="{SITE}/{imgs[0] if imgs else "assets/img/series/vol"+str(s)+".jpg"}">'))

# ── table of contents ────────────────────────────────────────
toc = f'<div class="wrap block"><h1 class="page">Mục lục — {len(arts)} kỳ</h1><p class="sub">Toàn bộ thư viện, xếp theo chuyên đề và thứ tự đọc.</p>'
for s in S_ORDER:
    rows = [r for r in arts if r['series'] == s]
    toc += f'''<section class="toc-sec">
  <h2><a href="series/s{s}/">Chuyên đề {s} — {esc(SERIES[s][0])}</a> <small>{len(rows)} kỳ</small></h2>
  <ol>{''.join(f'<li><a href="ky/{r["slug"]}/"><span class="toc-num">{r["ky"]}</span> {esc(r["title"])}</a></li>' for r in rows)}</ol>
</section>'''
toc += '</div>'
write('muc-luc/index.html', layout(f'Mục lục {len(arts)} kỳ — Hồ Sơ Thiên Hà', f'Danh sách đầy đủ {len(arts)} kỳ thuộc 9 chuyên đề.', toc, depth=1, canonical='/muc-luc/'))

# ── about ────────────────────────────────────────────────────
about = f'''<div class="wrap block prose-page">
<h1 class="page">Giới thiệu</h1>
<p><strong>Hồ Sơ Thiên Hà</strong> là một thư viện chuyên đề trực tuyến, chia sẻ miễn phí các nội dung về lịch sử thiên hà, di sản di truyền của loài người, các nền văn minh cổ đại và những phương pháp mở rộng nhận thức — được biên soạn thành 9 chuyên đề với {len(arts)} kỳ, sắp xếp theo một dòng thời gian liền mạch.</p>
<h2>Cách đọc</h2>
<p>Nếu là lần đầu, hãy bắt đầu từ <a href="series/s1/">Chuyên đề 1 — Tiền Sử Thiên Hà</a> và đọc tuần tự tới <a href="series/s9/">Chuyên đề 9 — Cẩm Nang Tâm Thức Vũ Trụ</a>. Mỗi kỳ chỉ 2.000 – 3.000 từ, đọc khoảng 10 phút, được thiết kế để đọc độc lập nhưng ăn khớp với mạch chung.</p>
<h2>Chính sách nội dung</h2>
<p>Toàn bộ nội dung được chia sẻ miễn phí cho mục đích nghiên cứu, tham khảo và mở rộng nhận thức. Đây là tài liệu tổng hợp từ nhiều nguồn công khai, không phải công bố của một tổ chức khoa học chính thống. Người đọc nên giữ tinh thần phản biện, đối chiếu và tự kiểm chứng — đó cũng chính là tinh thần mà bộ hồ sơ muốn truyền tải.</p>
<h2>Nội dung</h2>
<p>9 chuyên đề · {len(arts)} kỳ · {sum(r["nwords"] for r in arts):,} từ · {sum(len(r["imgs"]) for r in arts)} sơ đồ và hình minh họa.</p>
<p class="center"><a class="btn" href="muc-luc/">Vào mục lục</a></p>
</div>'''
write('gioi-thieu/index.html', layout('Giới thiệu — Hồ Sơ Thiên Hà', 'Hồ Sơ Thiên Hà: thư viện chuyên đề miễn phí về lịch sử thiên hà và tâm thức vũ trụ.', about, depth=1, canonical='/gioi-thieu/'))

# ── 404, sitemap, robots ─────────────────────────────────────
write('404.html', layout('Không tìm thấy trang — Hồ Sơ Thiên Hà', 'Trang không tồn tại.',
      '<div class="wrap block center"><h1 class="page">404</h1><p>Trang này không tồn tại. <a href="/">Về trang chủ</a> hoặc <a href="/muc-luc/">xem mục lục</a>.</p></div>', depth=0))
urls = ['/', '/series/', '/muc-luc/', '/gioi-thieu/'] + [f'/series/s{s}/' for s in S_ORDER] + [f'/ky/{r["slug"]}/' for r in arts]
today = datetime.date.today().isoformat()
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    pri = '1.0' if u == '/' else ('0.8' if u.startswith('/series/') else ('0.6' if u.startswith('/ky/') else '0.7'))
    sitemap += f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>\n'
sitemap += '</urlset>\n'
write('sitemap.xml', sitemap)
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('pages:', len(urls), '| articles:', len(arts))
