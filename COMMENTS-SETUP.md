# Bật bình luận ẩn danh — 5 phút

## 1. Tạo project Supabase (free)
https://supabase.com → Sign in (GitHub) → **New project**
- Tên: `hosothienha`
- Region: **Southeast Asia (Singapore)**
- Database password: đặt và lưu lại → Create

## 2. Chạy SQL
**SQL Editor** → dán toàn bộ `supabase-setup.sql` → **Run**

Kiểm tra: **Table Editor** → có bảng `comments`.

## 3. Lấy 2 giá trị
**Settings → API**:
- **Project URL**: `https://xxxxx.supabase.co`
- **anon public** key: chuỗi dài bắt đầu `eyJ...`

⚠️ KHÔNG dùng `service_role` key.

## 4. Điền vào `build_site.py`
Tìm 2 dòng gần đầu file:

```python
SUPABASE_URL = ''   # dán Project URL
SUPABASE_KEY = ''   # dán anon public key
```

Rồi:
```bash
python3 build_site.py
git add -A && git commit -m "Bật bình luận" && git push
```

## 5. Kiểm tra
Mở bất kỳ bài trong `/series/s1/...` → cuối bài có form. Gửi thử → reload → thấy hiện.

---

## Quản lý
**Table Editor → comments**: xoá dòng = xoá bình luận. Đặt `approved = false` = ẩn.

## Bảo mật
`anon` key chỉ cho phép: đọc bình luận đã duyệt + thêm mới. Không sửa, không xoá.
