(function () {
  var cfg = window.HSTH_COMMENTS;
  var root = document.getElementById('comments');
  if (!root || !cfg || !cfg.url || !cfg.key) return;

  var slug = root.getAttribute('data-slug');
  var API = cfg.url.replace(/\/$/, '') + '/rest/v1/comments';
  var H = {
    apikey: cfg.key,
    Authorization: 'Bearer ' + cfg.key,
    'Content-Type': 'application/json'
  };

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function ago(iso) {
    var d = (Date.now() - new Date(iso).getTime()) / 1000;
    if (d < 60) return 'vừa xong';
    if (d < 3600) return Math.floor(d / 60) + ' phút trước';
    if (d < 86400) return Math.floor(d / 3600) + ' giờ trước';
    if (d < 2592000) return Math.floor(d / 86400) + ' ngày trước';
    return new Date(iso).toLocaleDateString('vi-VN');
  }

  function render(list) {
    var box = root.querySelector('.cm-list');
    if (!list.length) {
      box.innerHTML = '<p class="cm-empty">Chưa có bình luận. Hãy là người đầu tiên.</p>';
      return;
    }
    box.innerHTML = list.map(function (c) {
      return '<article class="cm-item"><header><b>' + esc(c.author) +
        '</b><time>' + ago(c.created_at) + '</time></header><p>' +
        esc(c.body).replace(/\n/g, '<br>') + '</p></article>';
    }).join('');
  }

  function load() {
    fetch(API + '?slug=eq.' + encodeURIComponent(slug) +
          '&approved=eq.true&select=author,body,created_at&order=created_at.asc&limit=200',
          { headers: H })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(render)
      .catch(function () {
        root.querySelector('.cm-list').innerHTML = '<p class="cm-empty">Không tải được bình luận.</p>';
      });
  }

  var form = root.querySelector('form');
  var status = root.querySelector('.cm-status');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name.value.trim();
    var body = form.elements.body.value.trim();
    if (!name || !body) { status.textContent = 'Nhập tên và nội dung.'; return; }
    var btn = form.querySelector('button');
    btn.disabled = true; status.textContent = 'Đang gửi…';
    fetch(API, {
      method: 'POST',
      headers: Object.assign({}, H, { Prefer: 'return=minimal' }),
      body: JSON.stringify({ slug: slug, author: name, body: body })
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.elements.body.value = '';
      status.textContent = 'Đã gửi. Cảm ơn bạn!';
      load();
    }).catch(function () {
      status.textContent = 'Gửi thất bại. Thử lại sau ít phút.';
    }).finally(function () { btn.disabled = false; });
  });

  load();
})();
