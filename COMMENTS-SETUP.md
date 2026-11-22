# Bật bình luận — 5 phút

## 1. Tạo project Supabase (free)
1. https://supabase.com → Sign in (GitHub)
2. **New project** → đặt tên `hosothienha` → chọn region **Southeast Asia (Singapore)** → đặt database password (lưu lại) → Create

## 2. Chạy SQL
Mở **SQL Editor** → dán toàn bộ nội dung `supabase-setup.sql` → **Run**

Kiểm tra: **Table Editor** → thấy bảng `comments`.

## 3. Lấy 2 giá trị
**Settings → API**:
- **Project URL** → `https://xxxxx.supabase.co`
- **anon public** key (chuỗi dài bắt đầu `eyJ...`)

⚠️ **Không dùng `service_role` key** — key đó bỏ qua RLS, ai lấy được là xoá sạch database.

## 4. Điền vào build
Mở `build_site.py`, sửa 2 dòng đầu khối:

```python
SUPABASE_URL = 'https://xxxxx.supabase.co'
SUPABASE_KEY = 'eyJ...'          # anon public
```

Rồi:
```bash
python3 build_site.py
git add -A && git commit -m "Bật bình luận" && git push
```

## 5. Kiểm tra
Mở https://hosothienha.com/ky/<bài-bất-kỳ>/ → cuối bài có form. Gửi thử 1 bình luận → reload → thấy hiện.

---

## Quản lý bình luận
**Table Editor → comments**: xoá dòng = xoá bình luận. Sửa `approved = false` = ẩn.

## Chống spam
- Trigger SQL đã giới hạn 5 bình luận / 10 phút / 1 bài / 1 IP
- Nếu bị spam nặng: bật **Authentication → Providers → Email** và thêm captcha (Supabase hỗ trợ hCaptcha/Turnstile)

## Vì sao lộ anon key không sao
`anon` key chỉ cho phép đúng 2 việc theo RLS policy: **đọc bình luận đã duyệt** và **thêm bình luận mới**. Không sửa, không xoá, không đọc được bảng khác.
