/* Tìm kiếm client-side: 90 kỳ, index 47KB, không cần server. */
(function () {
  'use strict';

  var input = document.getElementById('q');
  var box = document.getElementById('results');
  if (!input || !box) return;

  var root = document.body.getAttribute('data-root') || '';
  var docs = null;
  var loading = false;

  // bỏ dấu tiếng Việt để tìm không cần gõ dấu
  function norm(s) {
    return String(s).toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'd');
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function hl(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (t.length < 2) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }

  function score(doc, terms) {
    var t = norm(doc.t), d = norm(doc.d);
    var n = norm(doc.t + ' ' + doc.d);
    var s = 0;
    for (var i = 0; i < terms.length; i++) {
      var q = terms[i];
      if (!q) continue;
      if (t.indexOf(q) !== -1) s += 30;
      else if (n.indexOf(q) !== -1) s += 8;
      // ưu tiên khớp đầu tên
      if (t.indexOf(q) === 0) s += 20;
      // khớp trọn từ
      if (new RegExp('(^|\\s)' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(\\s|$)', 'i').test(t)) s += 15;
    }
    return s;
  }

  function render(q) {
    var terms = norm(q).split(/\s+/).filter(Boolean);
    if (!terms.length) { box.innerHTML = ''; return; }
    var hits = docs
      .map(function (d) { return { d: d, s: score(d, terms) }; })
      .filter(function (x) { return x.s > 0; })
      .sort(function (a, b) { return b.s - a.s || a.d.k - b.d.k; })
      .slice(0, 30);

    if (!hits.length) {
      box.innerHTML = '<p class="s-empty">Không tìm thấy kết quả cho “' + esc(q) + '”.</p>';
      return;
    }
    box.innerHTML = '<p class="s-count">' + hits.length + ' kết quả</p>' +
      hits.map(function (x) {
        var d = x.d;
        return '<a class="s-item" href="' + root + d.u.slice(1) + '">' +
          '<span class="chip">Chuyên đề ' + d.s + ' · Kỳ ' + d.k + '</span>' +
          '<h3>' + hl(d.t, terms) + '</h3>' +
          '<p>' + hl(d.d.slice(0, 220), terms) + '</p>' +
          '</a>';
      }).join('');
  }

  function load() {
    if (docs || loading) return;
    loading = true;
    fetch(root + 'assets/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (json) {
        docs = json;
        loading = false;
        if (input.value.trim()) render(input.value);
      })
      .catch(function () {
        loading = false;
        box.innerHTML = '<p class="s-empty">Không tải được dữ liệu tìm kiếm.</p>';
      });
  }

  var timer;
  input.addEventListener('input', function () {
    if (!docs) load();
    clearTimeout(timer);
    timer = setTimeout(function () { render(input.value); }, 120);
  });
  input.addEventListener('focus', load);

  // hỗ trợ ?q=... để share link tìm kiếm
  var pq = new URLSearchParams(location.search).get('q');
  if (pq) { input.value = pq; load(); }
})();
