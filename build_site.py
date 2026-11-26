#!/usr/bin/env python3
"""Build static blog hosothienha.com from /tmp/site_content4.json (80 kỳ, 9 series)."""
import json, os, re, html, shutil, datetime

TODAY = datetime.date.today().isoformat()

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://hosothienha.com'
# ── Supabase comment backend (điền sau khi tạo project) ──
SUPABASE_URL = ''   # vd: https://abcdxyz.supabase.co
SUPABASE_KEY = ''   # anon public key

arts = json.load(open('/tmp/site_rebuild_src.json'))
arts.sort(key=lambda r: r['ky'])
import re as _re, html as _html
for _r in arts:
    _t = _html.unescape(_re.sub(r'<[^>]+>', ' ', _r['body']))
    _t = _re.sub(r'\s+', ' ', _t).strip()
    _r['nwords'] = len(_t.split())
    _r['lead'] = _r.get('lead') or (_t[:260].rsplit(' ', 1)[0] + '…')
    _r.setdefault('cover', _r['imgs'][0] if _r['imgs'] else 'assets/img/series/vol%d.jpg' % _r['series'])
    _r['path'] = 'series/s%d/%02d-%s' % (_r['series'], _r['ky'], _r['slug'])
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
 10: ('Lịch Sử Bị Che Giấu & Nền Văn Minh Cổ Đại', 'Lemuria, Atlantis, Đại Hồng Thủy, Khem, Great Tartaria, Mud Flood, Space Arks, NWO và sự thức tỉnh.'),
}
S_ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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
    ('/tim-kiem/', 'Tìm kiếm'),
]

def layout(title, desc, body, depth=0, canonical='/', extra_head='', comments=False):
    desc = desc.replace('80 kỳ', f'{len(arts)} kỳ')
    title = title.replace('80 kỳ', f'{len(arts)} kỳ')
    today = TODAY
    r = '../' * depth
    comments_scripts = ''
    if comments and SUPABASE_URL and SUPABASE_KEY:
        comments_scripts = (
            f'<script>window.HSTH_COMMENTS = {{"url": "{SUPABASE_URL}", "key": "{SUPABASE_KEY}"}};</script>\n'
            f'<script src="{r}assets/comments.js" defer></script>'
        )
    nav = ''.join(f'<a href="{r}{h.lstrip("/")}">{n}</a>' if h != '/' else f'<a href="{r or "./"}">{n}</a>'
                  for h, n in NAV)
    theme_toggle = '<button class="theme-toggle" id="themeToggle" aria-label="Chuyển đổi giao diện" title="Chế độ đọc">\n  <svg class="icon-sun" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>\n  <svg class="icon-moon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>\n</button>'
    theme_script = '<script>\n(function() {\n  const toggle = document.getElementById("themeToggle");\n  const sunIcon = toggle.querySelector(".icon-sun");\n  const moonIcon = toggle.querySelector(".icon-moon");\n  const html = document.documentElement;\n  \n  function applyTheme(theme) {\n    html.setAttribute("data-theme", theme);\n    localStorage.setItem("hsth-theme", theme);\n    if (theme === "dark") {\n      sunIcon.style.display = "block";\n      moonIcon.style.display = "none";\n    } else {\n      sunIcon.style.display = "none";\n      moonIcon.style.display = "block";\n    }\n  }\n  \n  const saved = localStorage.getItem("hsth-theme");\n  applyTheme(saved || "light");\n  \n  toggle.addEventListener("click", () => {\n    const current = html.getAttribute("data-theme");\n    applyTheme(current === "dark" ? "light" : "dark");\n  });\n})();\n</script>'

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
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="Đinh Trung Thành">
<meta name="theme-color" content="#111d33">
<meta property="og:locale" content="vi_VN">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/img/cover-full.jpg">
<meta property="og:image:width" content="900">
<meta property="og:image:height" content="1350">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/cover-full.jpg">
<link rel="alternate" hreflang="vi" href="{SITE}{canonical}">
<link rel="alternate" hreflang="x-default" href="{SITE}{canonical}">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"WebSite","@id":"{SITE}/#website","url":"{SITE}/","name":"Hồ Sơ Thiên Hà","description":"Thư viện chuyên đề miễn phí về lịch sử thiên hà, di sản di truyền và tâm thức vũ trụ.","inLanguage":"vi-VN","publisher":{{"@id":"{SITE}/#person"}},"potentialAction":{{"@type":"SearchAction","target":"{SITE}/muc-luc/?q={{search_term_string}}","query-input":"required name=search_term_string"}}}},{{"@type":"Person","@id":"{SITE}/#person","name":"Đinh Trung Thành","alternateName":"Jason Dinh","url":"{SITE}/gioi-thieu/","email":"dinhtrungthanh92@gmail.com"}}]}}</script>
{extra_head}
</head>
<body data-root="{r}">
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{r}"><span class="mark">✦</span> Hồ Sơ Thiên Hà</a>
    <nav class="nav">{nav}{theme_toggle}<a class="nav-search" href="{r}tim-kiem/" aria-label="Tìm kiếm">⌕</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <p><strong>Hồ Sơ Thiên Hà</strong> — thư viện chuyên đề miễn phí về lịch sử thiên hà, di sản di truyền và tâm thức vũ trụ.</p>
    <p>Tổng hợp & biên soạn: <strong>Đinh Trung Thành</strong> (Jason Dinh) · <a href="mailto:dinhtrungthanh92@gmail.com">dinhtrungthanh92@gmail.com</a></p>
    <p class="fine">10 chuyên đề · {len(arts)} kỳ · {sum(len(r["imgs"]) for r in arts)} hình minh họa · nội dung biên soạn và tổng hợp. Toàn bộ nội dung được chia sẻ miễn phí cho mục đích nghiên cứu và mở rộng nhận thức.</p>
    <div class="center" style="margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--line);">
      <p style="margin-bottom: 12px; font-size: 14px; color: var(--muted);">Ủng hộ duy trì thư viện</p>
      <img src="{r}assets/img/donate-qr.jpg" alt="QR code ủng hộ Hồ Sơ Thiên Hà" style="max-width: 160px; border-radius: 8px; box-shadow: 0 4px 16px -4px #0003;">
      <p style="margin-top: 8px; font-size: 12px; color: var(--muted);">Quét mã để ủng hộ</p>
    </div>
  </div>
</footer>
{comments_scripts}
    {theme_script}
</body>
</html>'''

def card(r, r_=''):
    return f'''<a class="card" href="{r_}{r['path']}/">
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
        <p class="lede">Từ Lăng Kính Lyra và các Đấng Sáng Lập, tới dòng máu Anunnaki, những nền văn minh lòng đất, chương trình không gian bí mật, hòm không gian cổ đại, hồ sơ các chủng tộc — và cuối cùng là cẩm nang tâm thức vũ trụ. 10 chuyên đề, {len(arts)} kỳ, đọc theo đúng mạch.</p>
        <form class="hero-search" action="tim-kiem/" method="get" role="search">
          <input type="search" name="q" placeholder="Tìm trong {len(arts)} kỳ — ví dụ: anunnaki, luân xa, agartha…" aria-label="Tìm kiếm">
          <button type="submit" aria-label="Tìm">Tìm</button>
        </form>
        <p class="actions"><a class="btn" href="muc-luc/">Xem mục lục {len(arts)} kỳ</a><a class="btn ghost" href="series/">Khám phá chuyên đề</a></p>
      </div>
      <figure class="hero-cover"><img src="assets/img/cover-full.jpg" alt="Bìa Hồ Sơ Thiên Hà — toàn tập 10 chuyên đề" fetchpriority="high"></figure>
    </div>
  </div>
</section>
<section class="block wrap">
  <h2 class="sec">10 chuyên đề</h2>
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
    f'{len(arts)} kỳ trong 10 chuyên đề: lịch sử thiên hà, dòng máu Anunnaki, văn minh lòng đất, chương trình không gian, hòm không gian cổ đại, hồ sơ chủng tộc, khoa học công nghệ và cẩm nang tâm thức.', home))

# ── series index + pages ─────────────────────────────────────
sbody = '<div class="wrap block"><h1 class="page">Chuyên đề</h1><p class="sub">10 tuyến truyện, ' + str(len(arts)) + ' kỳ. Bấm vào một chuyên đề để xem danh sách kỳ.</p><div class="sgrid">' + sercards_at('../') + '</div></div>'
write('series/index.html', layout('Chuyên đề — Hồ Sơ Thiên Hà', '10 chuyên đề về lịch sử thiên hà, di sản di truyền và tâm thức vũ trụ.', sbody, depth=1, canonical='/series/'))

for s in S_ORDER:
    rows = [r for r in arts if r['series'] == s]
    name, sub = SERIES[s]
    prev_s = S_ORDER[S_ORDER.index(s) - 1] if S_ORDER.index(s) > 0 else None
    next_s = S_ORDER[S_ORDER.index(s) + 1] if S_ORDER.index(s) < len(S_ORDER) - 1 else None
    kylist = ''.join(f'''<li><a href="../../{r['path']}/">
      <span class="chip">Kỳ {r['ky']}</span>
      <h3>{esc(r['title'])}</h3>
      <p>{esc(r['lead'])}</p>
      <span class="more">Đọc kỳ này →</span></a></li>''' for r in rows)
    navx = ''
    if prev_s: navx += f'<a class="btn ghost" href="../s{prev_s}/">← Chuyên đề {prev_s}: {esc(SERIES[prev_s][0])}</a> '
    if next_s: navx += f'<a class="btn ghost" href="../s{next_s}/">Chuyên đề {next_s}: {esc(SERIES[next_s][0])} →</a>'
    body = f'''<div class="wrap block">
  <p class="crumb"><a href="../../">Trang chủ</a> / <a href="../">Chuyên đề</a> / Chuyên đề {s}</p>
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
    s_schema = (f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage",'
                f'"@id":"{SITE}/series/s{s}/#series","name":"Chuyên đề {s}: {esc(name)}","description":"{esc(sub)}",'
                f'"inLanguage":"vi-VN","url":"{SITE}/series/s{s}/","isPartOf":{{"@type":"WebSite","@id":"{SITE}/#website"}},'
                f'"hasPart":[' + ','.join(
                    f'{{"@type":"Article","headline":"{esc(strip(rr["title"]))}","url":"{SITE}/{rr["path"]}/"}}'
                    for rr in rows) + ']}</script>')
    write(f'series/s{s}/index.html', layout(f'Chuyên đề {s}: {name} — Hồ Sơ Thiên Hà', sub, body, depth=2, canonical=f'/series/s{s}/', extra_head=s_schema))

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
    body_html = r['body']
    # Nếu body đã chèn ảnh inline (chuyên đề 10) thì không thêm cover/gallery tự động.
    if '<img' in body_html:
        cover = f'<figure class="art-fig"><img src="../../../{imgs[0]}" alt="{esc(r["title"])}" loading="lazy"></figure>' if imgs else ''
        figs_head = cover
        rest = []
    else:
     # opener cover image (first) + distribute the rest evenly between <h2> sections
     cover = f'<figure class="art-fig"><img src="../../../{imgs[0]}" alt="{esc(r["title"])}" loading="lazy"></figure>' if imgs else ''
     figs_head = cover
     rest = imgs[1:]
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
            fig = ''.join(f'<figure class="art-fig"><img src="../../../{i}" alt="{esc(r["title"])} — minh họa {n}" loading="lazy"></figure>' for n, i in enumerate(rest, 2))
            body_html = body_html + fig
        else:
            per = max(1, len(rest) // (len(blocks) - 1)) if len(blocks) > 1 else 1
            out, k = [blocks[0]], 0
            for bi, blk in enumerate(blocks[1:], 1):
                take = rest[k:k + per] if bi < len(rest) + 1 else []
                k += len(take)
                out.append(blk)
                for n, src in enumerate(take, 1):
                    out.append(f'<figure class="art-fig"><img src="../../../{src}" alt="{esc(r["title"])}" loading="lazy"></figure>')
            leftover = rest[k:]
            if leftover:
                out.append('<div class="gwrap">' + ''.join(
                    f'<figure><img src="../../../{src}" alt="{esc(r["title"])}" loading="lazy"></figure>' for src in leftover) + '</div>')
            body_html = ''.join(out)
    pager = '<div class="pager">'
    if prev_a: pager += f'<a class="pbtn" href="../../../{prev_a["path"]}/"><small>Kỳ trước</small><b>Kỳ {prev_a["ky"]} — {esc(prev_a["title"])[:70]}</b></a>'
    if next_a: pager += f'<a class="pbtn next" href="../../../{next_a["path"]}/"><small>Kỳ tiếp</small><b>Kỳ {next_a["ky"]} — {esc(next_a["title"])[:70]}</b></a>'
    pager += '</div>'

    body = f'''<div class="wrap article">
  <p class="crumb"><a href="../../../">Trang chủ</a> / <a href="../../">Chuyên đề {s}: {esc(name)}</a> / Kỳ {r['ky']}</p>
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
  <p class="center"><a class="btn ghost" href="../../../muc-luc/">Toàn bộ mục lục</a></p>
</div>'''
    write(f'{r["path"]}/index.html', layout(
        f'Kỳ {r["ky"]}: {strip(r["title"])} — {name}', strip(r['lead']), body, depth=3,
        canonical=f'/{r["path"]}/',
        extra_head=f'''<meta property="og:type" content="article">
<meta property="og:image" content="{SITE}/{imgs[0] if imgs else "assets/img/series/vol"+str(s)+".jpg"}">
<meta property="article:published_time" content="{TODAY}T00:00:00+11:00">
<meta property="article:author" content="Đinh Trung Thành">
<meta property="article:section" content="Chuyên đề {s}: {esc(name)}">
<script type="application/ld+json">{{"@context":"https://schema.org","@graph":[{{"@type":"Article","@id":"{SITE}/{r['path']}/#article","headline":"{esc(strip(r['title']))}","description":"{esc(strip(r['lead']))}","image":"{SITE}/{imgs[0] if imgs else "assets/img/series/vol"+str(s)+".jpg"}","inLanguage":"vi-VN","datePublished":"{TODAY}","dateModified":"{TODAY}","author":{{"@type":"Person","name":"Đinh Trung Thành","url":"{SITE}/gioi-thieu/"}},"publisher":{{"@type":"Person","name":"Đinh Trung Thành"}},"isPartOf":{{"@type":"CollectionPage","@id":"{SITE}/series/s{s}/#series","name":"Chuyên đề {s}: {esc(name)}"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"{SITE}/{r['path']}/"}}}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Trang chủ","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"Chuyên đề {s}: {esc(name)}","item":"{SITE}/series/s{s}/"}},{{"@type":"ListItem","position":3,"name":"Kỳ {r['ky']}: {esc(strip(r['title']))}","item":"{SITE}/{r['path']}/"}}]}}]}}</script>'''))

# ── table of contents ────────────────────────────────────────
toc = f'<div class="wrap block"><h1 class="page">Mục lục — {len(arts)} kỳ</h1><p class="sub">Toàn bộ thư viện, xếp theo chuyên đề và thứ tự đọc.</p>'
for s in S_ORDER:
    rows = [r for r in arts if r['series'] == s]
    toc += f'''<section class="toc-sec">
  <h2><a href="../series/s{s}/">Chuyên đề {s} — {esc(SERIES[s][0])}</a> <small>{len(rows)} kỳ</small></h2>
  <ol>{''.join(f'<li><a href="../{r["path"]}/"><span class="toc-num">{r["ky"]}</span> {esc(r["title"])}</a></li>' for r in rows)}</ol>
</section>'''
toc += '</div>'
write('muc-luc/index.html', layout(f'Mục lục {len(arts)} kỳ — Hồ Sơ Thiên Hà', f'Danh sách đầy đủ {len(arts)} kỳ thuộc 10 chuyên đề.', toc, depth=1, canonical='/muc-luc/'))

# ── about ────────────────────────────────────────────────────
about = f'''<div class="wrap block prose-page">
<h1 class="page">Giới thiệu</h1>
<h2>Người tổng hợp & biên soạn</h2>
<p><strong>Đinh Trung Thành</strong> (Jason Dinh) — người sáng lập và biên soạn toàn bộ thư viện này.</p>
<p>Qua nhiều năm nghiên cứu và tổng hợp, anh đã đọc, đối chiếu và hệ thống hóa hàng trăm nguồn tài liệu rời rạc — hồ sơ giải mật, văn bản cổ, truyền tin thiên hà, tài liệu nghiên cứu tâm thức — rồi ghép chúng thành một dòng thời gian có đầu có cuối, viết lại bằng tiếng Việt mạch lạc, bổ sung sơ đồ minh họa cho từng kỳ, và đưa lên web để bất kỳ ai cũng đọc được miễn phí.</p>
<p>Mục tiêu không phải thuyết phục người đọc tin vào một quan điểm, mà là trao cho họ một bản đồ đầy đủ để tự đối chiếu, tự kiểm chứng và tự đặt câu hỏi.</p>
<p>Liên hệ, góp ý hoặc báo lỗi nội dung: <a href="mailto:dinhtrungthanh92@gmail.com">dinhtrungthanh92@gmail.com</a></p>
<h2>Về thư viện</h2>
<p><strong>Hồ Sơ Thiên Hà</strong> là một thư viện chuyên đề trực tuyến, chia sẻ miễn phí các nội dung về lịch sử thiên hà, di sản di truyền của loài người, các nền văn minh cổ đại và những phương pháp mở rộng nhận thức — được biên soạn thành 10 chuyên đề với {len(arts)} kỳ, sắp xếp theo một dòng thời gian liền mạch.</p>
<h2>Cách đọc</h2>
<p>Nếu là lần đầu, hãy bắt đầu từ <a href="../series/s1/">Chuyên đề 1 — Tiền Sử Thiên Hà</a> và đọc tuần tự tới <a href="../series/s10/">Chuyên đề 10 — Lịch Sử Bị Che Giấu & Nền Văn Minh Cổ Đại</a>. Mỗi kỳ trung bình khoảng 1.650 từ, đọc chừng 7–10 phút, được thiết kế để đọc độc lập nhưng ăn khớp với mạch chung.</p>
<h2>Chính sách nội dung</h2>
<p>Toàn bộ nội dung được chia sẻ miễn phí cho mục đích nghiên cứu, tham khảo và mở rộng nhận thức. Đây là tài liệu tổng hợp từ nhiều nguồn công khai, không phải công bố của một tổ chức khoa học chính thống. Người đọc nên giữ tinh thần phản biện, đối chiếu và tự kiểm chứng — đó cũng chính là tinh thần mà bộ hồ sơ muốn truyền tải.</p>
<h2>Nội dung</h2>
<p>10 chuyên đề · {len(arts)} kỳ · hơn {round(sum(r["nwords"] for r in arts), -3):,} từ · {sum(len(r["imgs"]) for r in arts)} sơ đồ và hình minh họa.</p>
<h2>Hỗ trợ dự án</h2>
<p>Nếu bạn thấy giá trị từ thư viện này và muốn ủng hộ việc duy trì, mở rộng nội dung và phát triển thêm tính năng, có thể đóng góp qua QR code bên dưới. Mọi số tiền đều có ý nghĩa.</p>
<div class="center" style="margin: 32px 0;">
  <img src="../assets/img/donate-qr.jpg" alt="QR code ủng hộ Hồ Sơ Thiên Hà" style="max-width: 200px; border-radius: 8px; box-shadow: 0 4px 16px -4px #0003;">
  <p style="margin-top: 12px; font-size: 14px; color: var(--muted);">Quét mã để ủng hộ</p>
</div>
<p class="center"><a class="btn" href="../muc-luc/">Vào mục lục</a></p>
</div>'''
write('gioi-thieu/index.html', layout('Giới thiệu — Hồ Sơ Thiên Hà', 'Hồ Sơ Thiên Hà: thư viện chuyên đề miễn phí về lịch sử thiên hà và tâm thức vũ trụ.', about, depth=1, canonical='/gioi-thieu/'))

# ── search index ─────────────────────────────────────────────
def _plain(html_body):
    t = re.sub(r'<[^>]+>', ' ', html_body)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()

search_docs = []
for _r in arts:
    txt = _plain(_r['body'])
    search_docs.append({
        'u': '/' + _r['path'] + '/',
        't': strip(_r['title']),
        's': _r['series'],
        'k': _r['ky'],
        'd': strip(_r['lead']),
    })
write('assets/search-index.json', json.dumps(search_docs, ensure_ascii=False, separators=(',', ':')))

# ── search page ──────────────────────────────────────────────
search_body = f'''<div class="wrap block search-page">
  <h1 class="page">Tìm kiếm</h1>
  <p class="sub">Tìm theo tiêu đề hoặc nội dung — không cần gõ dấu tiếng Việt.</p>
  <div class="search-box">
    <input id="q" type="search" placeholder="Ví dụ: anunnaki, luân xa, solar warden…" autocomplete="off" autofocus>
  </div>
  <div id="results"></div>
</div>'''
write('tim-kiem/index.html', layout(f'Tìm kiếm — Hồ Sơ Thiên Hà', f'Tìm trong {len(arts)} kỳ của Hồ Sơ Thiên Hà.', search_body, depth=1, canonical='/tim-kiem/',
      extra_head='<script src="../assets/search.js" defer></script>'))

# ── 404, sitemap, robots ─────────────────────────────────────
write('404.html', layout('Không tìm thấy trang — Hồ Sơ Thiên Hà', 'Trang không tồn tại.',
      '<div class="wrap block center"><h1 class="page">404</h1><p>Trang này không tồn tại. <a href="/">Về trang chủ</a> hoặc <a href="/muc-luc/">xem mục lục</a>.</p></div>', depth=0))
urls = ['/', '/series/', '/muc-luc/', '/gioi-thieu/', '/tim-kiem/'] + [f'/series/s{s}/' for s in S_ORDER] + [f'/{r["path"]}/' for r in arts]
today = datetime.date.today().isoformat()
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    pri = '1.0' if u == '/' else ('0.8' if u.startswith('/series/') else ('0.6' if u.startswith('/ky/') else '0.7'))
    sitemap += f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><priority>{pri}</priority></url>\n'
sitemap += '</urlset>\n'
write('sitemap.xml', sitemap)
write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('pages:', len(urls), '| articles:', len(arts))
