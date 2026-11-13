#!/usr/bin/env python3
"""Generuje stanowiska.html z danych mapy Google My Maps (_src/map.kml).
Uruchamiany automatycznie przez _build.py."""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
KML = os.path.join(ROOT, "_src", "map.kml")


def coords(block):
    c = re.search(r"<coordinates>(.*?)</coordinates>", block, re.S).group(1).split()
    return [[round(float(y), 6), round(float(x), 6)] for x, y, *_ in (p.split(",") for p in c)]


def text(block, tag):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", block, re.S)
    if not m:
        return ""
    t = m.group(1)
    t = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", t, flags=re.S)
    t = html.unescape(t)
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return " ".join(t.replace("\xa0", " ").split())


def reservoir_of(num):
    n = int(re.match(r"\d+", num).group())
    return "duzy" if n < 30 else ("wyspy" if n < 39 else "wake")


def parse():
    s = open(KML, encoding="utf-8").read()
    data = {"stands": [], "reservoirs": [], "poi": [], "zones": [], "feeder": [], "lines": [], "dist": []}
    for folder in re.findall(r"<Folder>(.*?)</Folder>", s, re.S):
        fname = re.search(r"<name>(.*?)</name>", folder).group(1)
        for p in re.findall(r"<Placemark>(.*?)</Placemark>", folder, re.S):
            name = text(p, "name")
            desc = text(p, "description")
            if "<Point>" in p:
                ll = coords(p)[0]
                m = re.search(r"(?:Stanowisko|Domek|DOMEK)\s+(\d+[A-Za-z]?)", name)
                if fname == "ZBIORNIKI" and name.startswith("Zbiornik"):
                    key = "duzy" if "Duży" in name else ("wyspy" if "Wyspy" in name else "wake")
                    data["reservoirs"].append({"id": key, "name": name, "desc": desc, "ll": ll})
                elif m:
                    num = m.group(1).upper()
                    tags = []
                    if re.search(r"domek|domkiem", name + " " + desc, re.I) and not re.search(r"bez domku", desc, re.I):
                        tags.append("Domek")
                    if "VIP" in name.upper():
                        tags.append("VIP")
                    if "Premium" in desc[:80]:
                        tags.append("Premium")
                    depth = re.search(r"głębokoś\w*[^.]{0,40}?(około\s)?(\d[.,]\d+)\s?m(?:\s*(?:a|do|-)\s*(\d[.,]\d+)\s?m)?", desc, re.I)
                    rec = re.search(r"(\d{2}[,.]\d{1,3})\s?kg", desc)
                    data["stands"].append({
                        "id": num, "name": name.strip(), "res": reservoir_of(num), "desc": desc, "ll": ll,
                        "tags": tags, "depth": (("ok. " if depth.group(1) else "") + depth.group(2).replace(".", ",") + ("–" + depth.group(3).replace(".", ",") if depth.group(3) else "") + " m") if depth else "",
                        "rec": rec.group(1).replace(".", ",") + " kg" if rec else "",
                    })
                elif name.strip():
                    kind = "wc" if "WC" in name else ("parking" if "Parking" in name else
                           ("recepcja" if "Recepcja" in name else ("szlaban" if "SZLABAN" in name else "feeder")))
                    data["poi"].append({"kind": kind, "name": name.strip(), "desc": desc, "ll": ll})
            elif "<Polygon>" in p:
                (data["zones"] if "ZAKAZ" in name else data["feeder"]).append(coords(p))
            else:
                (data["dist"] if fname == "ODLEGŁOŚCI" else data["lines"]).append(
                    {"pts": coords(p), "label": name.strip()})
    order = lambda st: (int(re.match(r"\d+", st["id"]).group()), st["id"])
    data["stands"].sort(key=order)
    return data


RES_LABEL = {"duzy": "Zbiornik Duży", "wyspy": "Zbiornik Wyspy", "wake": "Zbiornik Wake"}


def body(head):
    d = parse()
    counts = {k: sum(1 for s in d["stands"] if s["res"] == k) for k in RES_LABEL}
    res_cards = "".join(
        f'<button class="res-card" data-res="{r["id"]}"><span class="res-n">{r["name"].split()[-1]}</span>'
        f'<b>{RES_LABEL[r["id"]]}</b><small>{counts[r["id"]]} stanowisk</small></button>'
        for r in sorted(d["reservoirs"], key=lambda r: list(RES_LABEL).index(r["id"])))
    payload = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return head("Mapa Stanowisk") + f"""
<section class="st-intro">
  <div class="wrap">
    <p class="lead">Wybierz zbiornik i stanowisko na mapie, przeczytaj opis, a potem zadzwoń. <strong>Rezerwacja tylko pod numerami telefonu:</strong></p>
    <div class="st-phones"><a class="tel" href="tel:+48509737377">509 737 377</a><a class="tel" href="tel:+48512464846">512 464 846</a></div>
  </div>
</section>
<section class="st-app" id="app">
  <div class="st-side">
    <div class="st-filter" role="tablist">
      <button class="on" data-res="all">Wszystkie</button>
      <button data-res="duzy">Duży</button><button data-res="wyspy">Wyspy</button><button data-res="wake">Wake</button>
      <button data-res="domek">Z domkiem</button>
    </div>
    <div class="st-res">{res_cards}</div>
    <div class="st-detail" id="detail" hidden></div>
    <ol class="st-list" id="list"></ol>
  </div>
  <div class="st-map"><div id="map" aria-label="Mapa stanowisk"></div>
    <div class="st-legend">
      <span><i class="lg-dot duzy"></i>Duży 36 ha</span><span><i class="lg-dot wyspy"></i>Wyspy 25 ha</span><span><i class="lg-dot wake"></i>Wake 18 ha</span>
      <span><i class="lg-sq"></i>domek</span><span><i class="lg-zone"></i>zakaz wędkowania</span>
    </div>
  </div>
</section>
<script id="st-data" type="application/json">{payload}</script>
<link rel="stylesheet" href="assets/leaflet/leaflet.css">
<script src="assets/leaflet/leaflet.js"></script>
<script src="assets/stanowiska.js"></script>
"""
