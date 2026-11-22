/* Chống copy cơ bản — chặn 95% người dùng thường.
   Không phải bảo mật thật: ai tắt JS hoặc dùng curl đều lấy được nội dung. */
(function () {
  'use strict';

  // ── 1. chặn menu chuột phải ──
  document.addEventListener('contextmenu', function (e) {
    if (e.target.closest('input, textarea, .comments')) return;
    e.preventDefault();
  }, false);

  // ── 2. chặn phím tắt copy / view-source / devtools ──
  document.addEventListener('keydown', function (e) {
    var k = (e.key || '').toLowerCase();
    var mod = e.ctrlKey || e.metaKey;

    // Ctrl/Cmd + C, A, S, P, U
    if (mod && ['c', 'a', 's', 'p', 'u'].indexOf(k) !== -1) {
      var el = e.target;
      if (el && el.closest && el.closest('input, textarea')) return;
      e.preventDefault();
      return false;
    }

    // F12
    if (k === 'f12') { e.preventDefault(); return false; }

    // Ctrl+Shift+I / J / C  (devtools)
    if (mod && e.shiftKey && ['i', 'j', 'c'].indexOf(k) !== -1) {
      e.preventDefault(); return false;
    }
  }, false);

  // ── 3. chặn kéo thả ảnh ──
  document.addEventListener('dragstart', function (e) {
    if (e.target && e.target.tagName === 'IMG') e.preventDefault();
  }, false);

  // ── 4. chặn copy qua selection ──
  document.addEventListener('copy', function (e) {
    var el = e.target;
    if (el && el.closest && el.closest('input, textarea')) return;
    var sel = String(window.getSelection() || '');
    if (sel.length > 60) {
      e.preventDefault();
      e.clipboardData.setData('text/plain',
        sel + '\n\n— Trích từ Hồ Sơ Thiên Hà · https://hosothienha.com');
    }
  }, false);

  // ── 5. mờ nội dung khi in (Ctrl+P đã chặn, phòng in từ menu) ──
  var st = document.createElement('style');
  st.textContent = '@media print{.prose{display:none!important}' +
    '.prose-print-notice{display:block!important;padding:40px;font-size:16px}' +
    '}';
  document.head.appendChild(st);

  // ── 6. cảnh báo console ──
  try {
    if (window.console && console.log) {
      console.log('%cHồ Sơ Thiên Hà',
        'font-size:20px;font-weight:700;color:#2f5da8');
      console.log('Nội dung được biên soạn và chia sẻ miễn phí. ' +
        'Vui lòng không sao chép hàng loạt — hãy chia sẻ link gốc.');
    }
  } catch (err) {}
})();
