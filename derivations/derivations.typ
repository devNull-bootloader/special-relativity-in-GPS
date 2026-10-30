#set document(title: "Relativistische Uhrkorrektionen in GPS: Vollständige Herleitungen")
#set page(numbering: "1")
#set text(font: "New Computer Modern", size: 11pt, lang: "de")
#set heading(numbering: "1.1")

#align(center, text(size: 24pt, weight: "bold")[
  Relativistische Uhrkorrektionen in GNSS-Satelliten
])

#align(center, text(size: 14pt)[
  Vollständige mathematische Herleitungen
])

#align(center, text(size: 11pt)[
  Jugend Forscht 2027 - Urvish Lanje
])


#outline(title: [Inhaltsverzeichnis], depth: 2, indent: 1em)

#line(length: 100%)

= Einleitung

Die GPS-Satelliten umkreisen die Erde mit einer Geschwindigkeit von etwa 3.873 m/s in einer Höhe von 20.200 km über der Erdoberfläche. Ihre Atomuhren ticken nicht mit der gleichen Rate wie Uhren auf der Erde wegen Einsteins Relativitätstheorie.

Zwei Effekte wirken gleichzeitig:

+ *Spezielle Relativität (SR):* Der bewegte Satellit; seine Uhr läuft langsamer
+ *Allgemeine Relativität (GR):* Der Satellit ist in einem schwächeren Gravitationsfeld; seine Uhr läuft schneller

Die Kombination dieser Effekte führt zu einer *Gesamtkorrektur von etwa +38,5 μs/Tag*, die im GPS-System berücksichtigt werden muss. Ohne diese Korrektur würde der Entfernungsfehler pro Satellit um etwa 11,5 km pro Tag wachsen.

Dieses Dokument leitet alle Korrektionen aus ersten Prinzipien her.

#line(length: 100%)


= Konstanten und Definitionen

Bevor man beginnt, definiert man die Konstanten:

#table(
  columns: (1fr, 2fr, 1fr),
  [*Symbol*], [*Bedeutung*], [*Wert*],
  [$G$], [Gravitationskonstante], [$6.674 times 10^(-11)$ m³/(kg·s²)],
  [$M_E$], [Erdmasse], [$5.972 times 10^(24)$ kg],
  [$c$], [Lichtgeschwindigkeit], [$2.998 times 10^8$ m/s],
  [$R_E$], [Erdradius], [$6.371 times 10^6$ m],
)

Für GPS-Satelliten: $h = 20.200$ km, $r = 26.570 times 10^6$ m, $e = 0.015$

#line(length: 100%)


= Spezielle Relativität

== Die Lichtuhr

Ein Photon springt zwischen zwei Spiegeln hin und her, getrennt durch Abstand $L$.

*Im Ruhesystem des Satelliten:*
$ t_0 = frac(2L, c) $

*Aus der Perspektive der Erde:* Das Photon folgt einem diagonalen Pfad. Nach Pythagoras:

$ L^2 + (frac(v t, 2))^2 = (frac(c t, 2))^2 $

Auflösen nach $t$:
$ t = frac(2L, sqrt(c^2 - v^2)) = t_0 times gamma $

wobei $gamma = frac(1, sqrt(1 - v^2/c^2))$ der *Lorentz-Faktor* ist.

== Schwache Feldnäherung

Für GPS ist $v^2/c^2$ sehr klein. Mit Reihenentwicklung:

$ gamma approx 1 + frac(v^2, 2c^2) $

Die Satellitenuhr misst die Eigenzeit $t_0 = t / gamma approx t (1 - v^2/(2c^2))$ und geht daher langsamer. Die Zeitdilatation über einen Tag:

$ Delta t_"SR" = -frac(v^2, 2c^2) times 86400 text(" s") $

== GPS Berechnung

Orbitalgeschwindigkeit:
$ v = sqrt(frac("GM", r)) = sqrt(frac(3.986 times 10^(14), 26.57 times 10^6)) approx 3873 text(" m/s") $

Zeitdilatation:
$ Delta t_"SR" = -frac((3873)^2, 2 times (2.998 times 10^8)^2) times 86400 approx -7.2 text(" μs/Tag") $

Das negative Vorzeichen zeigt, dass die Satellitenuhr *langsamer* läuft.

#line(length: 100%)

= Allgemeine Relativität

== Schwarzschild-Metrik

Für eine kugelsymmetrische Masse (Erde) ist die Zeitkomponente:

$ g_(t t) = 1 - frac(r_S, r) $

wobei $r_S = frac(2"GM", c^2)$ der *Schwarzschild-Radius* ist.

== Gravitationszeitdilatation

Eine ruhende Uhr bei Radius $r$ misst die Eigenzeit $d tau = sqrt(1 - r_S/r) d t$ ($d t$: Koordinatenzeit). Das Verhältnis der Zeitraten zwischen zwei Positionen ist daher:

$ frac(d tau_"sat", d tau_"ground") = frac(sqrt(1 - r_S/r_"orbit"), sqrt(1 - r_S/R_E)) $

Mit schwacher Feldnäherung:

$ frac(d tau_"sat", d tau_"ground") approx 1 + frac(r_S, 2) (frac(1, R_E) - frac(1, r_"orbit")) $

== GPS Berechnung

Schwarzschild-Radius der Erde:
$ r_S = frac(2 times 3.986 times 10^(14), (2.998 times 10^8)^2) = 8.87 times 10^(-3) text(" m") $

Mit $1 / R_E - 1 / r_"orbit" = 1.5696 times 10^(-7) - 0.3764 times 10^(-7) = 1.1932 times 10^(-7)$ 1/m ergibt sich die Gravitationszeitdilatation:
$ Delta t_"GR" = frac(r_S, 2) (frac(1, R_E) - frac(1, r_"orbit")) times 86400 $

$ approx 4.435 times 10^(-3) times 1.193 times 10^(-7) times 86400 approx +45.7 text(" μs/Tag") $

Das positive Vorzeichen zeigt, dass die Satellitenuhr *schneller* läuft.

#line(length: 100%)


= Kombinierte Korrektur

SR und GR wirken gleichzeitig:

$ Delta t_"net" = Delta t_"SR" + Delta t_"GR" = -7.2 + 45.7 = +38.5 text(" μs/Tag") $

Die Satellitenuhr geht also um $38.5$ μs pro Tag zu schnell. Deshalb wird ihre Frequenz vor dem Start um $Delta f / f approx -4.46 times 10^(-10)$ verringert. Ashby nennt $-446.47 times 10^(-12)$, das sind $38.57$ μs/Tag. Unser Wert weicht um etwa $0.2 %$ ab, weil das Kugelmodell das Quadrupolmoment der Erde und die Rotation der Bodenuhr nicht enthält.

== Entfernungsfehler ohne Korrektur

$ Delta x = c times Delta t = 2.998 times 10^8 times 38.5 times 10^(-6) = 11.54 text(" km/Tag") $

Ohne die relativistische Korrektur würde der Entfernungsfehler (Pseudorange) pro Satellit nach 24 Stunden *11,5 km* betragen.

#line(length: 100%)


= Die Nullpunkt-Höhe

Es gibt eine Höhe, wo SR und GR sich aufheben: $Delta t_"SR" + Delta t_"GR" = 0$.

Diese Herleitung ist eine bewusst vereinfachte Näherung. Die Bodenreferenz wird als ruhend im nicht rotierenden Bezugssystem behandelt; ihre eigene Erdrotationsgeschwindigkeit von ungefähr $465$ m/s am Äquator wird nicht berücksichtigt. Außerdem wird die Erde durch eine Kugel mit Radius $R_E$ beschrieben. Für eine reale Uhr auf dem WGS84-Geoid müssten die geographische Breite, die lokale Rotationsgeschwindigkeit, die Abplattung und das effektive Geopotential des Geoids einbezogen werden. Die folgenden $3186$ km sind daher nur der Nullpunkt dieses sphärischen Schwachfeldmodells.

Setzt man beide Korrektionen gleich null mit $v^2 = "GM"/r$:

$ -frac("GM", 2c^2 r) + frac("GM", c^2) (frac(1, R_E) - frac(1, r)) = 0 $

Vereinfachen:
$ -frac(1, 2r) - frac(1, r) + frac(1, R_E) = 0 $

$ frac(1, R_E) = frac(3, 2r) $

$ r = frac(3 R_E, 2) $

== Numerisch

$ r = frac(3 times 6.371 times 10^6, 2) = 9.557 times 10^6 text(" m") $

Höhe über der Erde:
$ h = r - R_E = 9.557 times 10^6 - 6.371 times 10^6 = 3.186 times 10^6 text(" m") = 3186 text(" km") $

Auf dieser Höhe tickt eine Uhr genauso schnell wie auf der Erde.

#line(length: 100%)


= Begrenzte Effekte

== Exzentrizität

Echte Satelliten haben elliptische Umlaufbahnen. Die Entfernung variiert:

$ r(nu) = frac(a(1 - e^2), 1 + e cos(nu)) $

Die periodische relativistische Korrektur einer elliptischen Bahn ist, bis auf ein konstantes Offset:

$ Delta t_"ecc" approx -frac(2 e sqrt(G M_E a), c^2) sin(E) $

Dabei ist $E$ die sogenannte exzentrische Anomalie. Für GPS mit $e = 0.015$ und $a approx 26.57 times 10^6$ m beträgt die Amplitude ungefähr $34$ ns.

*Herleitung (erste Ordnung in $e$):* Für eine Uhr im Orbit gilt

$ frac(d tau, d t) - 1 = -frac(G M, r c^2) - frac(v^2, 2 c^2) $

Mit der Vis-Viva-Gleichung und $r = a (1 - e cos(E))$ gilt

$ v^2 = G M (frac(2, r) - frac(1, a)) quad "und" quad frac(1, r) approx frac(1 + e cos(E), a) $

Damit folgt

$ frac(d tau, d t) - 1 approx -frac(3 G M, 2 a c^2) - frac(2 G M e, a c^2) cos(E) $

Der erste Term ist konstant (säkularer Anteil). Mit der Kepler-Gleichung gilt

$ d t = frac((1 - e cos(E)) d E, n) quad "mit" quad n = sqrt(frac(G M, a^3)) $

Die Integration des zweiten Terms ergibt in erster Ordnung

$ Delta t_"ecc" = -frac(2 G M e, a c^2 n) sin(E) = -frac(2 e sqrt(G M a), c^2) sin(E) $

== Sagnac-Effekt

Das Signal braucht ungefähr $70$ ms zum Empfänger. Weil sich die Erde währenddessen dreht, muss zusätzlich die Sagnac-Korrektur berücksichtigt werden:

$ Delta t_"Sagnac" = frac((bold(Omega) times bold(r)_"sat") dot bold(r)_"receiver", c^2) $

Dies ist die zusätzliche Laufzeit des Signals. Herleitung: In einem nicht rotierenden System bewegt sich der Empfänger mit $bold(v) = bold(Omega) times bold(r)_"receiver"$ während der Laufzeit

$ tau approx frac(|bold(r)_"sat" - bold(r)_"receiver"|, c) $

Bewegt er sich auf den Satelliten zu, wird der Weg kürzer. Die Wegänderung ist

$ -frac(bold(v) dot (bold(r)_"sat" - bold(r)_"receiver"), c) $

Geteilt durch $c$ ergibt das die Laufzeitänderung. Wegen $bold(v) dot bold(r)_"receiver" = 0$ folgt

$ Delta t_"Sagnac" = -frac((bold(Omega) times bold(r)_"receiver") dot bold(r)_"sat", c^2) $

Das ist der obige Ausdruck. Für die geozentrischen Vektoren bedeutet dies das Gleiche wie

$ Delta t_"Sagnac" = frac(Omega, c^2) (x_"sat" y_"receiver" - y_"sat" x_"receiver") $

Der Betrag ist höchstens

$ |Delta t_"Sagnac"| <= frac(Omega rho_"sat" rho_"receiver", c^2) $

wobei $rho$ der Abstand von der Erdachse ist. Für GPS sind das etwa $137$ ns für einen Empfänger am Äquator und etwa $83$ ns für Bremen im Modell.

#line(length: 100%)


= Zusammenfassung

#table(
  columns: (1.5fr, 1fr, 1fr),
  [*Effekt*], [*Typ*], [*Größe*],
  [Spezielle Relativität], [Linear], [-7.2 μs/Tag],
  [Allgemeine Relativität], [Linear], [+45.7 μs/Tag],
  [Nettokorrektur (GPS)], [Linear], [+38.5 μs/Tag],
  [Exzentrizität (GPS)], [Begrenzt], [±34 ns],
  [Sagnac-Fenster], [Begrenzt], [bis ±137 ns (Bremen: ±83 ns)],
)

#line(length: 100%)


= Referenzen

+ Ashby, Neil. "Relativity in the Global Positioning System." Living Reviews in Relativity 6, no. 1 (2003).
+ Space Systems Command (SSC). IS-GPS-200N: NAVSTAR GPS Space Segment/Navigation User Segment Interfaces. https://www.gps.gov/technical/icwg/IS-GPS-200N.pdf
