(function () {
  // menu mobilne
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // galeria - podgląd zdjęć
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lb]'));
  if (!links.length) return;
  var lb = document.createElement('div');
  lb.className = 'lb';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.innerHTML = '<img alt=""><button class="x" aria-label="Zamknij">×</button>' +
    '<button class="prev" aria-label="Poprzednie">‹</button><button class="next" aria-label="Następne">›</button>' +
    '<div class="count"></div>';
  document.body.appendChild(lb);
  var img = lb.querySelector('img'), count = lb.querySelector('.count'), cur = 0, group = [];

  function show(i) {
    cur = (i + group.length) % group.length;
    img.src = group[cur].href;
    img.alt = group[cur].querySelector('img').alt || '';
    count.textContent = (cur + 1) + ' / ' + group.length;
  }
  function close() { lb.classList.remove('open'); img.src = ''; document.body.style.overflow = ''; }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      group = links.filter(function (x) { return x.dataset.lb === a.dataset.lb; });
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      show(group.indexOf(a));
    });
  });
  lb.querySelector('.x').onclick = close;
  lb.querySelector('.prev').onclick = function () { show(cur - 1); };
  lb.querySelector('.next').onclick = function () { show(cur + 1); };
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });
  var sx = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
    sx = null;
  });
})();
