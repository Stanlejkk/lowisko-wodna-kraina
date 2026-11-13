(function () {
  var D = JSON.parse(document.getElementById('st-data').textContent);
  var RES = { duzy: 'Zbiornik Duży', wyspy: 'Zbiornik Wyspy', wake: 'Zbiornik Wake' };
  var listEl = document.getElementById('list');
  var detailEl = document.getElementById('detail');
  var resBox = document.querySelector('.st-res');
  var filterBtns = document.querySelectorAll('.st-filter button');

  var map = L.map('map', { zoomControl: true, scrollWheelZoom: true, maxZoom: 20 });
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxNativeZoom: 19, maxZoom: 20,
    attribution: 'Zdjęcia: Esri, Maxar, Earthstar Geographics'
  }).addTo(map);

  var allBounds = L.latLngBounds(D.stands.map(function (s) { return s.ll; }));
  map.fitBounds(allBounds, { padding: [30, 30] });

  // strefy
  D.zones.forEach(function (z) {
    L.polygon(z, { color: '#ba0a30', weight: 2, fillColor: '#ba0a30', fillOpacity: .28, dashArray: '4 4' })
      .bindTooltip('ZAKAZ WĘDKOWANIA', { sticky: true, className: 'st-tip' }).addTo(map);
  });
  D.feeder.forEach(function (z) {
    L.polygon(z, { color: '#ffcc00', weight: 2, fillColor: '#ffcc00', fillOpacity: .18 })
      .bindTooltip('FEEDER', { sticky: true, className: 'st-tip' }).addTo(map);
  });
  var lineLayer = L.layerGroup(D.lines.map(function (l) {
    return L.polyline(l.pts, { color: '#fff', weight: 1.5, opacity: .75, dashArray: '3 5', interactive: false });
  }));
  var distLayer = L.layerGroup(D.dist.map(function (l) {
    var pl = L.polyline(l.pts, { color: '#ffcc00', weight: 1.5, opacity: .9, interactive: false });
    if (l.label) pl.bindTooltip(l.label, { permanent: true, direction: 'center', className: 'st-dist' });
    return pl;
  }));
  function zoomLayers() {
    var z = map.getZoom();
    if (z >= 16) lineLayer.addTo(map); else map.removeLayer(lineLayer);
    if (z >= 18) distLayer.addTo(map); else map.removeLayer(distLayer);
  }
  map.on('zoomend', zoomLayers);

  // punkty usługowe
  var POI = { wc: 'WC', parking: 'P', recepcja: 'Recepcja', szlaban: 'Szlaban', feeder: 'Feeder' };
  D.poi.forEach(function (p) {
    var ic = L.divIcon({ className: '', html: '<span class="poi poi-' + p.kind + '">' + (POI[p.kind] || p.name) + '</span>', iconSize: null });
    var m = L.marker(p.ll, { icon: ic, keyboard: false }).addTo(map);
    m.bindTooltip(p.name + (p.desc ? ' – ' + p.desc : ''), { className: 'st-tip', direction: 'top', offset: [0, -10] });
  });

  // stanowiska
  var markers = {};
  D.stands.forEach(function (s) {
    var house = s.tags.indexOf('Domek') > -1;
    var ic = L.divIcon({
      className: '', iconSize: null,
      html: '<span class="pin ' + s.res + (house ? ' house' : '') + '">' + s.id + '</span>'
    });
    var m = L.marker(s.ll, { icon: ic, riseOnHover: true, title: s.name }).addTo(map);
    m.on('click', function () { select(s.id, false); });
    markers[s.id] = m;
  });

  zoomLayers();

  var filter = 'all';
  function match(s) {
    if (filter === 'all') return true;
    if (filter === 'domek') return s.tags.indexOf('Domek') > -1;
    return s.res === filter;
  }
  function esc(t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function renderList() {
    listEl.innerHTML = D.stands.filter(match).map(function (s) {
      var meta = [s.depth && ('głęb. ' + s.depth)].concat(s.tags).filter(Boolean).join(' · ');
      return '<li><button data-id="' + s.id + '"><span class="pin ' + s.res + (s.tags.indexOf('Domek') > -1 ? ' house' : '') + '">' + s.id + '</span>' +
        '<span class="li-t"><b>' + esc(s.name) + '</b><small>' + RES[s.res] + (meta ? ' · ' + esc(meta) : '') + '</small></span></button></li>';
    }).join('');
    D.stands.forEach(function (s) {
      var el = markers[s.id].getElement();
      if (el) el.classList.toggle('dim', !match(s));
    });
  }

  function setFilter(f, fit) {
    filter = f;
    filterBtns.forEach(function (b) { b.classList.toggle('on', b.dataset.res === f); });
    resBox.hidden = f !== 'all';
    renderList();
    if (fit !== false) {
      var pts = D.stands.filter(match).map(function (s) { return s.ll; });
      if (pts.length) map.flyToBounds(pts, { padding: [40, 40], duration: .6 });
    }
  }

  function showDetail(htmlStr) {
    detailEl.innerHTML = htmlStr;
    detailEl.hidden = false;
    listEl.hidden = true; resBox.hidden = true;
    detailEl.querySelector('.back').onclick = clearSel;
    detailEl.parentNode.scrollTop = 0;
  }

  var current = null;
  function select(id, fromList) {
    var s = D.stands.filter(function (x) { return x.id === id; })[0];
    if (!s) return;
    if (current && markers[current].getElement()) markers[current].getElement().classList.remove('sel');
    current = id;
    var el = markers[id].getElement(); if (el) el.classList.add('sel');
    map.flyTo(s.ll, Math.max(map.getZoom(), 17), { duration: .6 });
    var facts = '';
    if (s.depth) facts += '<div><small>Głębokość</small><b>' + s.depth + '</b></div>';
    if (s.rec) facts += '<div><small>Największa ryba</small><b>' + s.rec + '</b></div>';
    facts += '<div><small>Zbiornik</small><b>' + RES[s.res].replace('Zbiornik ', '') + '</b></div>';
    showDetail(
      '<button class="back">← Wszystkie stanowiska</button>' +
      '<div class="d-head"><span class="pin big ' + s.res + (s.tags.indexOf('Domek') > -1 ? ' house' : '') + '">' + s.id + '</span>' +
      '<div><h2>' + esc(s.name) + '</h2><p class="d-tags">' + s.tags.map(function (t) { return '<span>' + t + '</span>'; }).join('') + '</p></div></div>' +
      '<div class="d-facts">' + facts + '</div>' +
      (s.desc ? '<p class="d-desc">' + esc(s.desc) + '</p>' : '<p class="d-desc">Opis stanowiska wkrótce.</p>') +
      '<div class="d-cta"><span>Zarezerwuj stanowisko ' + s.id + ':</span><a href="tel:+48509737377">509 737 377</a><a href="tel:+48512464846">512 464 846</a></div>'
    );
    history.replaceState(null, '', '#s' + id);
  }

  function selectRes(id) {
    var r = D.reservoirs.filter(function (x) { return x.id === id; })[0];
    setFilter(id);
    showDetail(
      '<button class="back">← Wszystkie stanowiska</button>' +
      '<div class="d-head"><div><h2>' + esc(r.name) + '</h2></div></div>' +
      '<p class="d-desc">' + esc(r.desc) + '</p>' +
      '<p class="d-more"><button class="link" data-res="' + id + '">Pokaż stanowiska na tym zbiorniku →</button></p>'
    );
    detailEl.querySelector('.link').onclick = function () { clearSel(); setFilter(id, false); };
    history.replaceState(null, '', '#' + id);
  }

  function clearSel() {
    if (current && markers[current].getElement()) markers[current].getElement().classList.remove('sel');
    current = null;
    detailEl.hidden = true; listEl.hidden = false; resBox.hidden = filter !== 'all';
    history.replaceState(null, '', location.pathname);
  }

  listEl.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-id]'); if (b) select(b.dataset.id, true);
  });
  filterBtns.forEach(function (b) {
    b.addEventListener('click', function () { clearSel(); setFilter(b.dataset.res); });
  });
  resBox.addEventListener('click', function (e) {
    var b = e.target.closest('.res-card'); if (b) selectRes(b.dataset.res);
  });

  renderList();
  var h = location.hash.slice(1);
  if (h[0] === 's' && h.length > 1) select(h.slice(1).toUpperCase());
  else if (RES[h]) selectRes(h);
})();
