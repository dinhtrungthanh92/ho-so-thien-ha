# Hồ Sơ Thiên Hà — blog chuyên đề

Static site (GitHub Pages) tại https://hosothienha.com

- 9 chuyên đề · 80 kỳ · 548 sơ đồ/hình minh họa
- Build: `python3 build_site.py` (nguồn nội dung: `/tmp/site_content4.json`)
- Deploy: push lên `main` → GitHub Pages tự phục vụ từ thư mục gốc

## Cấu trúc
| Đường dẫn | Nội dung |
|---|---|
| `index.html` | Trang chủ |
| `series/s1..s9/` | Trang chuyên đề |
| `muc-luc/` | Mục lục 80 kỳ |
| `ky/<slug>/` | Trang từng kỳ |
| `gioi-thieu/` | Giới thiệu |
| `assets/img/ky/` | Ảnh minh họa từng kỳ (nén 1100px) |
| `assets/img/series/` | Bìa 9 chuyên đề |
| `sitemap.xml`, `robots.txt` | SEO |
