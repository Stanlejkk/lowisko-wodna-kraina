#!/usr/bin/env python3
"""Generuje statyczne strony HTML nowej wersji lowiskowodnakraina.pl.
Treść przepisana 1:1 ze starej strony (_src/*.html). Uruchom: python3 _build.py"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))

REZ = "http://wioskarybackawilga.pl/index.php/rezerwacja-lowisko"
FB = "https://www.facebook.com/lowiskowodnakraina"
MAP_BIG = ("https://maps.google.pl/maps?f=q&amp;source=embed&amp;hl=pl&amp;geocode=&amp;q=stawowa+wilga&amp;aq=&amp;sll=52.24755,21.193789"
           "&amp;sspn=5.590628,16.907959&amp;ie=UTF8&amp;hq=stawowa+wilga&amp;hnear=&amp;t=m&amp;cid=268278736515707126"
           "&amp;ll=51.852322,21.374588&amp;spn=0.12724,0.174408&amp;z=11&amp;iwloc=A")
MAP_EMBED = "https://maps.google.com/maps?q=Stawowa+9,+08-470+Wilga&amp;z=12&amp;output=embed"

NAV = [
    ("index.html", "Strona Główna"),
    ("onas.html", "O Nas"),
    ("gatunki.html", "Gatunki Ryb"),
    ("oplaty.html", "Opłaty"),
    ("galeria.html", "Galeria"),
    ("regulamin.html", "Regulamin"),
    ("kontakt.html", "Kontakt"),
]

KPO_TEXT = ('Beneficjent MMW Sp. z o.o. realizuje projekt pt. "Dywersyfikacja działalności prowadzonej przez MMW Sp. z o.o." '
            'przy wsparciu finansowym z Unii Europejskiej. Głównym celem projektu jest rozszerzenie i dywersyfikacja działalności, '
            'która pozwoli uodpornić się na przyszłe niekorzystne sytuacje losowe związane z sytuacją pandemiczną i kryzysową.')

PARTNERS = [
    ("https://ng24.pl/", "ng.png", "NG"),
    ("http://normark.pl/", "normark.png", "Normark"),
    ("https://www.facebook.com/PBProductspl/", "pb.png", "PB Products"),
    ("https://www.aquavu.com/", "aq.png", "Aqua-Vu"),
    ("https://rozemeijer.com/", "roz.png", "Rozemeijer"),
    ("https://carplive.pl/", "clive.png", "Carp Live"),
    (None, "4s.png", "Partner"),
]


def partners_html():
    out = []
    for href, img, alt in PARTNERS:
        tag = f'<img src="img/{img}" alt="{alt}" width="250" height="100" loading="lazy">'
        out.append(f'<a href="{href}" target="_blank" rel="noopener">{tag}</a>' if href else f'<span>{tag}</span>')
    return '<div class="partners">' + "".join(out) + '</div>'


HOURS = """<dl class="hours">
  <dt>Poniedziałek - Piątek</dt><dd>08:00 - 21:00</dd>
  <dt>Sobota</dt><dd>08:00 - 21:00</dd>
  <dt>Niedziela</dt><dd>08:00 - 21:00</dd>
  <dd class="carp">Dla Karpiarzy 24h</dd>
</dl>"""


def aside(extra=""):
    return f"""<aside class="aside">
  <div class="tiles">
    <a class="tile" href="wyp.html">Wypożyczalnia <span>→</span></a>
    <a class="tile alt" href="domki.html">Noclegi <span>→</span></a>
  </div>
  <section class="card"><h2>Godziny otwarcia</h2>{HOURS}</section>
  <section class="card"><h2>Dojazd</h2>
    <iframe class="map-frame" src="{MAP_EMBED}" loading="lazy" title="Mapa dojazdu - Wilga, ul. Stawowa 9"></iframe>
    <a class="small-link" href="{MAP_BIG}" target="_blank" rel="noopener">Wyświetl większą mapę →</a>
  </section>{extra}
</aside>"""


def page(slug, title, desc, body, current=None):
    nav = "".join(
        '<a href="'+h+'"'+(' aria-current="page"' if h == current else '')+'>'+t+'</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="wodna kraina, łowisko wędkarskie, wilga, ryby, wędkowanie, łowisko karpiowe, karp, szczupak, okoń, tołpytga, lin, karaś">
<meta name="theme-color" content="#3d0f00">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,500;0,700;1,400&amp;family=Alegreya+Sans:wght@400;500;700&amp;family=Big+Shoulders+Display:wght@700;800;900&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="img/gatunki/karp.png">
</head>
<body>

<div class="kpo-bar">
  <div class="wrap">
    <img src="img/kpo.jpg" alt="Krajowy Plan Odbudowy, Rzeczpospolita Polska, Sfinansowane przez Unię Europejską NextGenerationEU" width="800" height="103">
    <p>Projekt „Dywersyfikacja działalności prowadzonej przez MMW Sp. z o.o.” · Wkład Funduszy Europejskich: 511.096,41 PLN · Umowa nr: KPOD.01.03-IW.01-A585/24</p>
    <a href="oprojekcie.html">O projekcie →</a>
  </div>
</div>

<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" title="Łowisko Wodna Kraina"><img src="img/logo.png" alt="Łowisko Wodna Kraina w Wildze" width="308" height="150"></a>
    <button class="burger" aria-expanded="false" aria-controls="nav">Menu ☰</button>
    <nav class="nav" id="nav" aria-label="Menu główne">{nav}<a class="btn-rez" href="{REZ}" target="_blank" rel="noopener">Rezerwacja</a></nav>
    <a class="btn-rez" href="{REZ}" target="_blank" rel="noopener">Rezerwacja</a>
  </div>
</header>

<main id="tresc">
{body}
</main>

<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <img class="logo-f" src="img/logostopka.png" alt="Łowisko Wodna Kraina" width="243" height="79">
      <p>Z dala od wielkich miast, w malowniczej dolinie Wisły, pośród lasów, wrzosowisk i sadów.</p>
      <p><a href="{FB}" target="_blank" rel="noopener">Facebook: /lowiskowodnakraina</a></p>
    </div>
    <div>
      <h2>Kontakt</h2>
      <p>MMW Sp. z o.o.<br>08-470 Wilga, ul. Stawowa 9</p>
      <p><a href="tel:+48512464846">512 464 846</a> · <a href="tel:+48509737377">509 737 377</a><br>
      Opiekun łowiska: <a href="tel:+48600619482">600 619 482</a><br>
      <a href="mailto:rezerwacjewilga@wp.pl">rezerwacjewilga@wp.pl</a></p>
    </div>
    <div>
      <h2>Godziny otwarcia</h2>
      <p>Poniedziałek - Piątek: 08:00 - 21:00<br>Sobota: 08:00 - 21:00<br>Niedziela: 08:00 - 21:00<br><b style="color:#fff">Dla Karpiarzy 24h</b></p>
    </div>
  </div>
  <div class="wrap foot-partners">
    <h2>Nasi Partnerzy</h2>
    {partners_html()}
  </div>
  <div class="wrap foot-bottom">Wszelkie prawa zastrzeżone - www.lowiskowodnakraina.pl</div>
  <div class="foot-kpo">
    <div class="wrap">
      <img src="img/kpo.jpg" alt="KPO" width="800" height="103" loading="lazy">
      <div>
        <p>{KPO_TEXT}</p>
        <p>Wysokość wkładu Funduszy Europejskich: 511.096,41PLN · Umowa nr: KPOD.01.03-IW.01-A585/24 · <a href="oprojekcie.html">O PROJEKCIE</a></p>
      </div>
    </div>
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""


def head(title, crumb=True):
    c = f'<p class="crumbs"><a href="index.html">Strona Główna</a> / {title}</p>' if crumb else ""
    return f'<section class="page-head"><div class="wrap">{c}<h1 class="rise">{title}</h1></div></section>'


# ------------------------------------------------------------------ galerie
def parse_gallery(name):
    s = open(os.path.join(ROOT, "_src", name + ".html"), encoding="utf-8").read()
    s = s[s.find('id="lewa"'):s.find('id="prawa"')]
    secs, cur = [], None
    for m in re.finditer(r'<font[^>]*>([^<]+)</font>|<a href="(img/galeria/[^"]+)"[^>]*><img src="(img/galeria/[^"]+)"', s):
        if m.group(1):
            cur = {"title": " ".join(m.group(1).split()), "imgs": []}
            secs.append(cur)
        else:
            full, mini = m.group(2), m.group(3)
            if not (os.path.isfile(os.path.join(ROOT, full)) and os.path.isfile(os.path.join(ROOT, mini))):
                continue
            if cur is None:
                cur = {"title": "", "imgs": []}; secs.append(cur)
            cur["imgs"].append((full, mini))
    return [x for x in secs if x["imgs"]]


GTABS = [("galeria.html", "Łowisko"), ("zarybianie.html", "Zarybianie"), ("zdobycze.html", "Zdobycze"), ("zawody.html", "Zawody")]


def gallery_body(name, fname):
    tabs = '<nav class="tabs" aria-label="Galerie">' + "".join(
        '<a href="'+h+'"'+(' aria-current="page"' if h == fname else '')+'>'+t+'</a>' for h, t in GTABS) + "</nav>"
    out = []
    for i, sec in enumerate(parse_gallery(name)):
        imgs = "".join(
            f'<a href="{html.escape(f)}" data-lb="g{i}"><img src="{html.escape(m)}" alt="{html.escape(sec["title"])}" loading="lazy"></a>'
            for f, m in sec["imgs"])
        out.append(f'<section class="gallery-sec"><h2 class="h2">{html.escape(sec["title"])} <small>{len(sec["imgs"])} zdjęć</small></h2><div class="grid">{imgs}</div></section>')
    return head("Galeria") + f'<div class="wrap layout full"><div>{tabs}{"".join(out)}</div></div>'


# ------------------------------------------------------------------ strony
PAGES = {}

PAGES["index"] = ("Wodna Kraina - Łowisko Wędkarskie - Wilga - Rodzinny Park Rozrywki - Strona Głowna",
"Z dala od wielkich miast, w malowniczej dolinie Wisły, pośród lasów, wrzosowisk i sadów rozciąga się kompleks stawów gdzie umiejscowione jest łowisko wodna kraina oraz rodzinny park rozrywki.",
f"""
<section class="hero">
  <div class="hero-grid">
    <div class="hero-txt">
      <p class="kicker rise">Witamy · Wilga, ul. Stawowa 9</p>
      <h1 class="rise d2">Łowisko<span>Wodna Kraina</span></h1>
      <p class="hero-lead rise d3">Dla miłośników wędkarstwa stworzyliśmy szereg łowisk obfitujące w różnorodne gatunki ryb.</p>
      <div class="hero-hours rise d4">
        <span>Poniedziałek - Niedziela</span><b>08:00 - 21:00</b>
        <span>Dla Karpiarzy</span><b>24h</b>
      </div>
      <div class="hero-actions rise d4">
        <a class="btn btn-gold" href="{REZ}" target="_blank" rel="noopener">Mapa stanowisk - rezerwacja</a>
        <a class="btn" href="oplaty.html">Cennik</a>
      </div>
    </div>
    <div class="hero-photo"><img src="img/galeria/lowisko/20.JPG" alt="Zachód słońca nad łowiskiem Wodna Kraina" width="900" height="675"></div>
  </div>
</section>

<section class="notice" aria-label="Komunikat">
  <div class="wrap">
    <strong>Uwaga</strong>
    <p>W związku z nowymi opłatami od dzisiejszego dnia na łowisku wodna kraina wprowadzamy opłatę za śmieci worek 120 l - 20 zł. Zachęcamy do wywożenia swoich śmieci z terenu łowiska, wówczas opłaty nie będą naliczane. Za utrudnienia PRZEPRASZAMY.</p>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="prose">
      <h2>Wędkarstwo w Wildze</h2>
      <p class="lead">Cały nasz obiekt to powierzchni 150 h, z czego większość to jeziora, stawy, lasy, położone w malowniczej, turystycznej miejscowości podwarszawskiej Wildze.</p>
      <p>Przez ponad 25 lat w chronionych stawach, bez żadnej ingerencji ze strony człowieka wytworzyły się populacje dużych osobników. Dominują karpie o wielkości od 5kg do 25 kg, amury od 8kg do 20 kg i szczupaki od 5 kg do 20 kg.</p>
      <p>Zapraszamy głównie wędkarzy, miłośników ciszy, obcowania z przyrodą i wędkarstwa sportowego, dla których zasada to <strong>„Złów i Wypuść”</strong> – znajdziecie u nas dużą rybę i wymarzony odpoczynek. Kierujemy się zasadą bezwzględnego zakazu zabijania i zabierania ryb.</p>
      <p>Łowiska są czynne od świtu do zmierzchu, dla karpiarzy całą dobę. Głębokość łowiska od 1,5 metra do 3 metrów.</p>
      <p>Zapraszamy również do organizacji zawodów i mistrzostw wędkarskich na terenie naszego łowiska.</p>
      <div class="facts">
        <div><b>150 ha</b><small>jeziora, stawy, lasy</small></div>
        <div><b>25+ lat</b><small>chronionych stawów</small></div>
        <div><b>5–25 kg</b><small>karpie</small></div>
        <div><b>1,5–3 m</b><small>głębokość łowiska</small></div>
      </div>
    </div>
    <div>
      <figure class="mapblock" style="margin:0"><img src="img/mapka.jpg" alt="Mapka naszych łowisk: staw Alka-Bekas 15 ha, Czajka 3,5 ha, Kulik 25 ha, Irysowski 36 ha" width="560" height="754"></figure>
      <a class="reserve" href="{REZ}" target="_blank" rel="noopener">
        <span><h3>Mapa Stanowisk</h3><p>kliknij i wybierz stanowisko</p></span>
        <span class="arrow">→</span>
      </a>
    </div>
  </div>
</section>

<section class="band water">
  <div class="wrap split">
    <img src="img/glowna.png" alt="Pomost na łowisku Wodna Kraina" width="550" height="280" style="width:100%;border:8px solid #fff">
    <div>
      <h2 class="h2" style="margin-top:0">Godziny otwarcia</h2>
      {HOURS}
      <div class="tiles" style="margin-top:28px">
        <a class="tile" href="wyp.html">Wypożyczalnia <span>→</span></a>
        <a class="tile alt" href="domki.html">Noclegi <span>→</span></a>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div>
      <h2 class="h2" style="margin-top:0">Dojazd</h2>
      <iframe class="map-frame" style="aspect-ratio:4/3" src="{MAP_EMBED}" loading="lazy" title="Mapa dojazdu - Wilga, ul. Stawowa 9"></iframe>
      <a class="small-link" href="{MAP_BIG}" target="_blank" rel="noopener">Wyświetl większą mapę →</a>
    </div>
    <div>
      <h2 class="h2" style="margin-top:0">Nasi Partnerzy</h2>
      {partners_html()}
    </div>
  </div>
</section>
""")

PAGES["onas"] = ("O Nas - Łowisko Wodna Kraina - Wilga",
"Łowisko Wodna Kraina w Wildze - o nas i okolica.",
head("O Nas") + f"""
<div class="wrap layout">
<article class="prose">
<p class="lead">Dla miłośników wędkarstwa stworzyliśmy szereg łowisk obfitujące w różnorodne gatunki ryb.</p>
<p>Cały nasz obiekt to powierzchni 150 h, z czego większość to jeziora, stawy, lasy, położone w malowniczej, turystycznej miejscowości podwarszawskiej Wildze.</p>
<p>Przez ponad 25 lat w chronionych stawach, bez żadnej ingerencji ze strony człowieka wytworzyły się populacje dużych osobników. Dominują karpie o wielkości od 5kg do 25 kg, amury od 8kg do 20 kg i szczupaki od 5 kg do 20 kg.</p>
<h3>Gatunki ryb występujące w naszych stawach</h3>
<ul class="floats cols-3">
<li>karpie</li><li>amury</li><li>karasie</li><li>szczupaki</li><li>okonie</li><li>liny</li><li>sandacze</li><li>tołpygi</li><li>płocie</li>
</ul>
<p>Zapraszamy głównie wędkarzy, miłośników ciszy, obcowania z przyrodą i wędkarstwa sportowego, dla których zasada to „Złów i Wypuść” – znajdziecie u nas dużą rybę i wymarzony odpoczynek. Kierujemy się zasadą bezwzględnego zakazu zabijania i zabierania ryb.</p>
<p>Łowiska są czynne od świtu do zmierzchu. Głębokość łowiska od 1,5 metra do 3 metrów.</p>
<p>Zapraszamy również do organizacji zawodów i mistrzostw wędkarskich na terenie naszego łowiska.</p>

<h2>Okolica</h2>
<p>Z dala od wielkich miast, w malowniczej dolinie Wisły, pośród lasów, wrzosowisk i sadów rozciąga się jedyna w tym regionie, turystyczna gmina Wilga należąca do powiatu Garwolińskiego, położona w odległości około 50 km od Warszawy.</p>
<p>Gmina Wilga - rzadko zaludniona (5200 osób mieszka na 119 km2), obdarzona wspaniałym klimatem i mało dotąd zmienionym przez człowieka krajobrazem, jest wymarzonym miejscem wypoczynku. Sosnowe lasy na wydmach wytwarzają korzystne dla zdrowia olejki eteryczne. Ciągnące się wzdłuż Wisły pasmo urodzajnych gleb madowych sprzyja rozwojowi ogrodnictwa oraz sadownictwa. Znajdujące się na terenie Gminy Osiedle Wypoczynkowe w kulminacyjnych miesiącach letnich, zamieszkałe jest przez właścicieli 5 tysięcy prywatnych działek rekreacyjnych.</p>
<p>Co daje nam w sezonie nawet do 25 tysięcy turystów.</p>
<p>Gmina Wilga ma też zaszczyt posiadać na swoim terenie w Rudzie Talubskiej Wypoczynkowy Ośrodek Prezydencki.</p>
<p>Wilga jest gniazdem rodu Wilckich, a lokowana jako miasto była przed rokiem 1554. Najważniejszym zabytkiem gminy jest kościół Księży Marianów w Mariańskim Porzeczu - Goźlinie, o unikalnej konstrukcji zrębowej naśladującej formy architektury murowanej. W trzynawowym wnętrzu można zobaczyć późnobarokową, iluzjonistyczną polichromię z drugiej połowy XVIII wieku.</p>
<p>W okolicach Wilgi nie brak pomnikowych drzew. Najpiękniejsze okazy to dąb im. gen. Józefa Dwernickiego w leśniczówce Cyganówka oraz dwa dęby szypułkowe na cmentarzu w Wildze.</p>
<p>Wydmy w okolicach Mariańskiego Porzecza porasta dwuigłowa sosna Banksa wywodząca się z Ameryki Północnej.</p>
<p>W Wildze i jej okolicach odnajdziemy wiele miejsc pamięci narodowej. Dla upamiętnienia zaciętych walk, podczas przeprawy wojsk w 1944 roku na przyczółek warecko - magnuszewski, wzniesiono pomnik saperów.</p>
<figure class="mapblock" style="margin:30px 0 0;max-width:483px"><img src="img/mapa.jpg" alt="Mapa okolicy Wilgi" width="483" height="599" loading="lazy"></figure>
</article>
{aside()}
</div>""")

SPECIES = [("karp", "Karp"), ("szczupak", "Szczupak"), ("sandacz", "Sandacz"), ("amur", "Amur"), ("karas", "Karaś"),
           ("tolpyga", "Tołpyga"), ("okon", "Okoń"), ("sum", "Sum"), ("lin", "Lin"), ("leszcz", "Leszcz"), ("ploc", "Płoć")]
PAGES["gatunki"] = ("Gatunki Ryb - Łowisko Wodna Kraina - Wilga",
"Gatunki ryb na łowisku Wodna Kraina w Wildze: karp, szczupak, sandacz, amur, karaś, tołpyga, okoń, sum, lin, leszcz, płoć.",
head("Gatunki Ryb") + f"""
<div class="wrap layout">
<article>
<p class="lead" style="margin-top:0">Wszystkie gatunki ryb występują na wszystkich naszych zbiornikach.</p>
<div class="records">
  <div><small>Rekord</small><b>24,8 kg</b><span>Karp</span></div>
  <div><small>Rekord</small><b>132 cm</b><span>Szczupak</span></div>
  <div><small>Rekord</small><b>22 kg</b><span>Amur</span></div>
  <div><small>Rekord</small><b>85 cm</b><span>Sandacz</span></div>
</div>
<div class="species">
{"".join(f'<figure><img src="img/gatunki/{f}.png" alt="{n}" width="270" height="150" loading="lazy"></figure>' for f, n in SPECIES)}
</div>
</article>
{aside()}
</div>""")


def price(what, cost, note="", unit=""):
    n = f"<small>{note}</small>" if note else ""
    u = f"<small>{unit}</small>" if unit else ""
    return f'<div class="price"><span class="what">{what}{n}</span><span class="dots"></span><span class="cost">{cost}{u}</span></div>'


PAGES["oplaty"] = ("Opłaty - Cennik i rezerwacja - Łowisko Wodna Kraina - Wilga",
"Cennik łowiska karpiowego i łowiska z drapieżnikami, wypożyczalnia sprzętu i łódek - Wodna Kraina Wilga.",
head("Opłaty") + f"""
<div class="wrap layout">
<article>
<p class="kicker" style="color:var(--splawik)">Cennik i rezerwacja</p>

<section class="price-group">
<h2 class="h2">Łowiska karpiowego</h2>
{price("Zezwolenie na dobę dla jednego wędkarza", "100zł", "jedna doba (trzy wędki) Niedziela - czwartek", "jedna doba")}
{price("Zasiadka piątek - niedziela", "240zł", "", "2 doby / jedna osoba")}
{price("Każda następna wędka", "20zł", "Zezwolenie pozwala na łowienie na trzy wędki każda następna wędka to dopłata w wysokości 20zł")}
{price("Osoba towarzysząca", "20 zł", "Osoba towarzysząca uiszcza opłatę w wysokości 20 zł za dzień.", "za dzień")}
{price("Dowóz sprzętu quadem z przyczepką", "10zł", "Dowozimy sprzęt wędkarski w każde miejsce na łowisku quadem z przyczepką.", "za jeden przejazd")}
{price("Zezwolenie na dobę dla jednego wędkarza feeder / spławik", "70zł", "jeden dzień (dwie wędki)", "jeden dzień")}
<div class="callout gold">Posiadamy gratisowe wózki wędkarskie dla łowiących na transport sprzętu wędkarskiego.</div>
</section>

<section class="price-group">
<h2 class="h2">Łowiska z drapieżnikami</h2>
{price("Zezwolenie na dzień dla jednego wędkarza", "120zł", "", "dzień")}
{price("Osoba towarzysząca", "20 zł", "Osoba towarzysząca uiszcza opłatę w wysokości 20 zł za dzień.", "za dzień")}
{price("Dowóz sprzętu quadem z przyczepką", "10zł", "Dowozimy sprzęt wędkarski w każde miejsce na łowisku quadem z przyczepką.", "za jeden przejazd")}
<div class="callout gold">Posiadamy gratisowe wózki wędkarskie dla łowiących na transport sprzętu wędkarskiego.</div>
<div class="callout"><b>Doliczana jest opłata za śmieci 1 worek 120 l - 20zł</b></div>
</section>

<section class="price-group">
<h2 class="h2">Wypożyczenie</h2>
{price("Komplet - drewniane wiosła z dulkami, mata, podbierak", "50 zł")}
{price("Drewniane wiosła z dulkami", "25 zł", "", "dzień")}
{price("Podbierak karpiowy", "30 zł", "", "doba")}
{price("Kołyska karpiowa", "30 zł", "", "doba")}
{price("Sling karpiowy", "30 zł", "", "doba")}
{price("Ponton karpiowy", "60 zł", "", "+ kaucja / doba")}
</section>

<section class="price-group">
<h2 class="h2">Sprzęt</h2>
{price("Dwie zielone łódki wędkarskie (2 osoby)", "50zł", "", "dzień")}
{price("Duża łódka wędkarska biała (4 osoby)", "60zł", "", "dzień")}
{price("Duża łódka wędkarska pomarańczowa (4 osoby)", "60zł", "", "dzień")}
{price("Łódka wędkarska biało-bordowa (2 osoby)", "50zł", "", "dzień")}
{price("Łódka wędkarska biało-pomarańczowa (2 osoby)", "50zł", "", "dzień")}
{price("Łódka wędkarska biało-czerwona (2 osoby)", "50zł", "", "dzień")}
{price("Wodowanie własnej łódki lub pontonu", "20zł")}
<div class="callout"><b>Nasze łódki nie posiadają w standardzie wyposażenia.</b> Koszt wynajęcia wioseł wraz z dulkami, kotwicą - 50zł / dzień.</div>

<h3 class="h2" style="font-size:1.6rem;margin-top:1.4em">Nasz Sprzęt</h3>
<div class="boats">
  <figure><img src="img/sprzet/lodkabiala.JPG" alt="Łódka Biała" width="800" height="531" loading="lazy"><figcaption>Łódka Biała</figcaption></figure>
  <figure><img src="img/sprzet/lodkapomaranczowa.JPG" alt="Łódka Pomarańczowa" width="800" height="577" loading="lazy"><figcaption>Łódka Pomarańczowa</figcaption></figure>
  <figure><img src="img/sprzet/lodkazielona.JPG" alt="Łódka Zielona" width="800" height="477" loading="lazy"><figcaption>Łódka Zielona</figcaption></figure>
</div>
<div class="prose">
<p>Łódki nie posiadają silników elektrycznych oraz typowych wioseł wędkarskich, uchwytów dulka.<br>
Na wyposażeniu łódek posiadamy wiosła kajakowe, obciążenia granitowe.<br>
Zachęcamy do korzystania z własnych silników elektrycznych.</p>
</div>
</section>

<section class="price-group">
<h2 class="h2">Cennik za 1kg złowionej ryby</h2>
{price("Karaś", "15zł", "", "kg")}
<div class="callout"><b>UWAGA WĘDKARZE !!</b><br>Wszystkie złowione ryby wypuszczamy z powrotem do łowiska, wyjątek stanowi karaś - 1kg 15zł.</div>
</section>
</article>
{aside()}
</div>""")

PAGES["wyp"] = ("Wypożyczalnia - Łowisko Wodna Kraina - Wilga",
"Cennik sprzętu w wypożyczalni łowiska Wodna Kraina w Wildze.",
head("Wypożyczalnia") + f"""
<div class="wrap layout">
<article>
<p class="kicker" style="color:var(--splawik)">Cennik sprzętu</p>
<div class="boats">
  <figure><img src="img/pod.jpg" alt="Podbierak" width="936" height="512" loading="lazy"><figcaption>Podbierak <em>25 zł</em></figcaption></figure>
  <figure><img src="img/mat.jpg" alt="Mata" width="900" height="396" loading="lazy"><figcaption>Mata <em>25 zł</em></figcaption></figure>
  <figure><img src="img/sprzet/lodkabiala.JPG" alt="Łódka Biała" width="800" height="531" loading="lazy"><figcaption>Łódka Biała <em>50 zł</em></figcaption></figure>
  <figure><img src="img/sprzet/lodkapomaranczowa.JPG" alt="Łódka Pomarańczowa" width="800" height="577" loading="lazy"><figcaption>Łódka Pomarańczowa <em>50 zł</em></figcaption></figure>
  <figure><img src="img/sprzet/lodkazielona.JPG" alt="Łódka Zielona" width="800" height="477" loading="lazy"><figcaption>Łódka Zielona <em>50 zł</em></figcaption></figure>
  <figure><img src="img/sprzet/rowerek.JPG" alt="Rowerek Wodny - Platforma" width="800" height="529" loading="lazy"><figcaption>Rowerek Wodny - Platforma <em>50 zł</em></figcaption></figure>
</div>
</article>
{aside()}
</div>""")

PAGES["domki"] = ("Noclegi - Łowisko Wodna Kraina - Wilga",
"Nowa usługa noclegowa z cateringiem - mobilne kontenery 4-osobowe nad brzegiem zbiornika wędkarskiego.",
head("Noclegi") + f"""
<div class="wrap layout">
<article class="prose">
<p class="kicker" style="color:var(--splawik)">Nowość 2026</p>
<h2>Nowa usługa noclegowa z cateringiem</h2>
<p class="lead">Oferujemy Państwu noclegi w nowoczesnych, mobilnych kontenerach 4-osobowych z możliwością skorzystania z całodziennego cateringu.</p>
<p>Bazowa lokalizacja kontenerów znajduje się na Polanie Dzikiej Gęsi, bezpośrednio nad brzegiem zbiornika wędkarskiego. Takie usytuowanie umożliwia gościom korzystanie na wyłączność z pomostów wędkarskich znajdujących się w tej strefie.</p>
<p>Regulamin łowiska dostępny jest na stronie: <a href="regulamin.html">lowiskowodnakraina.pl</a></p>
<p>W przypadku wyboru przez klienta innej lokalizacji na terenie naszego obiektu, do ceny pobytu doliczany jest koszt transportu oraz ustawienia kontenera.</p>
<p>Nasze nowe mobilne kontenery są w pełni umeblowane, wyposażone w mini aneksy kuchenne oraz klimatyzację, co zapewnia komfortowy pobyt niezależnie od pogody.</p>
<p>Dodatkowo oferujemy możliwość skorzystania z całodziennego cateringu, który – na życzenie klienta – dostarczany jest bezpośrednio do kontenera. Menu dostępne jest na stronie: <a href="http://www.tawernanadstawami.pl" target="_blank" rel="noopener">www.tawernanadstawami.pl</a></p>
<p>Dla osób preferujących tradycyjną formę wyżywienia polecamy również menu stacjonarne restauracji Tawerna nad Stawami, działającej na terenie kompleksu.</p>

<div class="split" style="gap:32px;margin-top:30px">
  <section><h3 style="margin-top:0">Cennik noclegów | 2026</h3>
    {price("1 doba", "150 zł", "", "doba | osoba")}
    {price("2 doby", "120 zł", "", "doba | osoba")}
    {price("3 doby i więcej", "100 zł", "", "doba | osoba")}
  </section>
  <section><h3 style="margin-top:0">Wędkowanie | 2026</h3>
    {price("Piątek - niedziela", "120 zł", "", "doba | osoba")}
    {price("Niedziela - piątek", "100 zł", "", "doba | osoba")}
  </section>
</div>
<p style="margin-top:24px"><strong>Wilga | Stawowa 9</strong></p>
<figure style="margin:36px 0 0"><img class="poster" src="img/domki2026.png" alt="Plakat: Nowość 2026 - nowa usługa noclegowa z cateringiem" width="800" height="1000" loading="lazy"></figure>
</article>
{aside()}
</div>""")

PAGES["kontakt"] = ("Kontakt - Łowisko Wodna Kraina - Wilga",
"Kontakt: MMW Sp. z o.o., 08-470 Wilga, ul. Stawowa 9. Tel. 512 464 846, 509 737 377.",
head("Kontakt") + f"""
<div class="wrap layout">
<article>
<div class="contact-grid">
  <div><h2>Firma</h2><p><strong>MMW Sp. z o.o.</strong><br>08-470 Wilga, ul. Stawowa 9</p><p style="margin-top:10px"><strong>NIP</strong> 8262217408</p></div>
  <div><h2>Telefon Kontaktowy</h2><a class="tel" href="tel:+48512464846">512 464 846</a><a class="tel" href="tel:+48509737377">509 737 377</a></div>
  <div><h2>Opiekun łowiska, informacje, porady</h2><a class="tel" href="tel:+48600619482">600 619 482</a></div>
  <div><h2>E-mail</h2><a class="tel" style="font-size:1.45rem" href="mailto:rezerwacjewilga@wp.pl">rezerwacjewilga@wp.pl</a></div>
</div>
<iframe class="map-frame" style="aspect-ratio:16/9;margin-top:36px" src="{MAP_EMBED}" loading="lazy" title="Mapa dojazdu - Wilga, ul. Stawowa 9"></iframe>
</article>
{aside()}
</div>""")

PAGES["oprojekcie"] = ("O projekcie - KPO - Łowisko Wodna Kraina - Wilga",
"Projekt Dywersyfikacja działalności prowadzonej przez MMW Sp. z o.o. - Krajowy Plan Odbudowy.",
head("O projekcie") + f"""
<div class="wrap layout">
<article class="prose">
<img src="img/kpo.jpg" alt="Krajowy Plan Odbudowy, Rzeczpospolita Polska, Sfinansowane przez Unię Europejską NextGenerationEU" width="800" height="103" style="margin-bottom:28px">
<p>Beneficjent MMW Sp. z o.o. realizuje projekt pt. "Dywersyfikacja działalności prowadzonej przez MMW Sp. z o.o." przy wsparciu finansowym z Unii Europejskiej. Głównym celem projektu jest rozszerzenie i dywersyfikacja działalności, która pozwoli uodpornić się na przyszłe niekorzystne sytuacje losowe związane z sytuacją pandemiczną i kryzysową. Przedmiotem inwestycji jest zabezpieczenie ciągłości działalności gospodarczej oraz wprowadzenie zmian wpływających na budowanie odporności firmy MMW Sp. z o.o. na przyszłe kryzysy poprzez zakup środków trwałych oraz wprowadzenie do oferty nowej usługi w postaci usług noclegowych (krótkotrwałego zakwaterowania) z cateringiem.</p>
<h3>Zakres przedsięwzięcia</h3>
<p><strong>1. Zakup środków trwałych:</strong></p>
<ul class="floats">
<li>1.1. Mobilny kontener kempingowy – 8 szt.</li>
<li>1.2. Instalacja fotowoltaiczna o mocy 33 kW wraz z magazynem energii 30 kW</li>
<li>1.3. Piec konwekcyjno-parowy wraz z podstawą</li>
<li>1.4. Witryna chłodnicza nastawna 58l</li>
<li>1.5. Nadstawka chłodnicza 9xGN 1/3</li>
<li>1.6. Nadstawka chłodnicza 12xGN 1/3</li>
</ul>
<p>Dzięki zakupowi realizacji przedmiotowej inwestycji Wnioskodawca skutecznie dostosuje swój model działalności, ograniczając wpływ COVID-19 i skutków spowodowanych przez niego kryzysu w przedsiębiorstwie, a także rozszerzy grupę potencjalnych klientów. Usługa noclegowa (krótkotrwałego zakwaterowania) z cateringiem będzie skierowana głównie do wędkarzy, klientów łowisk. Usługa będzie świadczona przez cały rok, co przyczyni się do wzrostu liczby klientów korzystających z oferty usługowej Wnioskodawcy i pozwoli na realizację dłuższych, rodzinnych pobytów.</p>
<div class="facts" style="margin-top:20px">
  <div><b>698.498,42 PLN</b><small>Całkowity koszt projektu</small></div>
  <div><b>511.096,41 PLN</b><small>Wysokość wkładu Funduszy Europejskich</small></div>
</div>
<p style="margin-top:18px">Umowa nr: KPOD.01.03-IW.01-A585/24</p>
</article>
{aside()}
</div>""")


# regulamin: treść 1:1 ze starej strony
def regulamin():
    s = open(os.path.join(ROOT, "_src", "regulamin.html"), encoding="utf-8").read()
    s = s[s.find('id="lewa"'):s.find('id="prawa"')]
    a = s.find("Karpiowy regulamin"); b = s.find("REGULAMIN ŁOWISKA Z DRAPIEŻNIKAMI")
    carp_raw = html.unescape(s[a:b])
    carp_raw = carp_raw[carp_raw.find("1. Na łowisku"):]
    carp_raw = carp_raw[:carp_raw.find("</p>")]
    carp = [re.sub(r"^\d+\.\s*", "", x.strip()) for x in re.split(r"<br\s*/?>", carp_raw) if x.strip()]
    pred_raw = s[b:]
    pred_raw = pred_raw[pred_raw.find("1. Łowisko"):]
    pred_raw = pred_raw[:pred_raw.find("UWAGA!")]
    pred_items = re.split(r"(?:<br\s*/?>\s*)+(?=\s*(?:<font[^>]*>\s*)?(?:<b>)?\s*\d+\.)", pred_raw)

    def clean(t):
        warn = "FF0000" in t
        t = re.sub(r"<(?!/?b>)[^>]+>", " ", t)
        t = re.sub(r"<br\s*/?>", " ", t)
        t = " ".join(t.split())
        t = re.sub(r"^(<b>\s*)?\d+\.\s*", lambda m: m.group(1) or "", t)
        t = re.sub(r"<b>\s*</b>", "", t)
        return t, warn

    def carp_li(t):
        if t.startswith("Na łowisku obowiązuje zakaz:"):
            head_, rest = t.split(":", 1)
            parts = [p.strip() for p in re.split(r"\s-\s", " " + rest) if p.strip()]
            tail = ""
            last = parts[-1]
            k = last.find(". ")
            if k > 0:
                parts[-1], tail = last[:k + 1], last[k + 2:]
            return f"<li>{head_}:<ul>" + "".join(f"<li>{p}</li>" for p in parts) + f"</ul>{(' <strong>' + tail + '</strong>') if tail else ''}</li>"
        return f"<li>{t}</li>"

    carp_html = "".join(carp_li(t) for t in carp)
    pred_html = ""
    for it in pred_items:
        t, warn = clean(it)
        if not t:
            continue
        t = t.replace("<b>", "").replace("</b>", "")
        if t.startswith("A) "):
            pass
        t = re.sub(r"\s([BC]\))", r"<br>\1", t)
        pred_html += f'<li class="warn">{t}</li>' if warn else f"<li>{t}</li>"

    body = head("Regulamin Łowiska") + f"""
<div class="wrap layout">
<article>
<nav class="tabs" aria-label="Regulaminy"><a href="#karpiowy" aria-current="page">Łowisko karpiowe</a><a href="#drapieznik">Łowisko z drapieżnikami</a></nav>
<h2 class="h2" id="karpiowy" style="margin-top:0">Karpiowy regulamin Łowiska Wilga Wodna Kraina 2025</h2>
<ol class="rules">{carp_html}</ol>
<h2 class="h2" id="drapieznik">Regulamin łowiska z drapieżnikami</h2>
<ol class="rules">{pred_html}</ol>
<div class="callout"><b>UWAGA!</b> W przypadku ryb ważących powyżej 18 kg przed wypuszczeniem obowiązuje natychmiastowe powiadomienie opiekuna łowiska!</div>
</article>
{aside()}
</div>"""
    return body


PAGES["regulamin"] = ("Regulamin Łowiska - Wodna Kraina - Wilga",
"Regulamin łowiska karpiowego i łowiska z drapieżnikami - Wodna Kraina Wilga.", regulamin())

GAL_META = {
    "galeria": "Galeria - Łowisko Wodna Kraina - Wilga",
    "zarybianie": "Galeria - Zarybianie - Łowisko Wodna Kraina - Wilga",
    "zdobycze": "Galeria - Zdobycze - Łowisko Wodna Kraina - Wilga",
    "zawody": "Galeria - Zawody - Łowisko Wodna Kraina - Wilga",
}

if __name__ == "__main__":
    for slug, (title, desc, body) in PAGES.items():
        cur = f"{slug}.html" if f"{slug}.html" in dict(NAV) else None
        with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as fh:
            fh.write(page(slug, title, desc, body, cur))
    for slug, title in GAL_META.items():
        with open(os.path.join(ROOT, f"{slug}.html"), "w", encoding="utf-8") as fh:
            fh.write(page(slug, title, "Galeria zdjęć łowiska Wodna Kraina w Wildze.", gallery_body(slug, f"{slug}.html"), "galeria.html"))
    print("OK:", ", ".join(list(PAGES) + list(GAL_META)))
