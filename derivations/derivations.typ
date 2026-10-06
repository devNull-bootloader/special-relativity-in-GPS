#set document(title: "Relativistische Uhrkorrektionen in GPS: Vollständige Herleitungen")
#set page(numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set heading(numbering: "1.1")

#align(center, text(size: 24pt, weight: "bold")[
  Relativistische Uhrkorrektionen in GNSS-Satelliten
])

#align(center, text(size: 14pt)[
  Vollständige mathematische Herleitungen
])

#align(center, text(size: 11pt, style: "italic")[
  Jugend Forscht 2027 - Urvish Lanje
])

#align(center, text(size: 10pt, fill: gray)[
  September 2026
])

---

= Inhaltsverzeichnis

#outline(depth: 2, indent: 1em)

---

= Einleitung

Die GPS-Satelliten umkreisen die Erde mit einer Geschwindigkeit von etwa 3.874 m/s in einer Höhe von 20.200 km über der Erdoberfläche. Ihre Atomuhren ticken nicht mit der gleichen Rate wie Uhren auf der Erde wegen Einsteins Relativitätstheorie.

Zwei Effekte wirken gleichzeitig:

+ *Spezielle Relativität (SR):* Der bewegte Satellit; seine Uhr läuft langsamer
+ *Allgemeine Relativität (GR):* Der Satellit ist in einem schwächeren Gravitationsfeld; seine Uhr läuft schneller

Die Kombination dieser Effekte führt zu einer *Gesamtkorrektur von etwa +38,5 μs/Tag*, die im GPS-System berücksichtigt werden muss. Ohne diese Korrektur würde die Positionsgenauigkeit um etwa 11,5 km pro Tag abnehmen.

Dieses Dokument leitet alle Korrektionen aus ersten Prinzipien her.

#line(length: 100%)


= Konstanten und Definitionen

Bevor man beginnt, definiert man die Konstanten:

#table(
  columns: (1fr, 2fr, 1fr),
  [*Symbol*], [*Bedeutung*], [*Wert*],
  [$G$], [Gravitationskonstante], [$6.674 times 10^{-11}$ m³/(kg·s²)],
  [$M_E$], [Erdmasse], [$5.972 times 10^{24}$ kg],
  [$c$], [Lichtgeschwindigkeit], [$3 times 10^8$ m/s],
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

Die Zeitdilatation über einen Tag:

$ Delta t_"SR" = -frac(v^2, 2c^2) times 86400 text(" s") $

== GPS Berechnung

Orbitalgeschwindigkeit:
$ v = sqrt(frac("GM", r)) = sqrt(frac(3.986 times 10^{14}, 26.57 times 10^6)) = 3874 text(" m/s") $

Zeitdilatation:
$ Delta t_"SR" = -frac((3874)^2, 2 times (3 times 10^8)^2) times 86400 approx -7.2 text(" μs/Tag") $

Das negative Vorzeichen zeigt, dass die Satellitenuhr *langsamer* läuft.

#line(length: 100%)

= Allgemeine Relativität

== Schwarzschild-Metrik

Für eine kugelsymmetrische Masse (Erde) ist die Zeitkomponente:

$ g_{t t} = 1 - frac(r_S, r) $

wobei $r_S = frac(2"GM", c^2)$ der *Schwarzschild-Radius* ist.

== Gravitationszeitdilatation

Das Verhältnis der Zeitraten zwischen zwei Positionen:

$ frac(d t_"sat", d t_"ground") = frac(sqrt(1 - r_S/r_"orbit"), sqrt(1 - r_S/R_E)) $

Mit schwacher Feldnäherung:

$ frac(d t_"sat", d t_"ground") approx 1 + frac(r_S, 2) (frac(1, R_E) - frac(1, r_"orbit")) $

== GPS Berechnung

Schwarzschild-Radius der Erde:
$ r_S = frac(2 times 3.986 times 10^{14}, (3 times 10^8)^2) = 8.87 times 10^{-3} text(" m") $

Gravitationszeitdilatation:
$ Delta t_"GR" = frac(r_S, 2) (frac(1, R_E) - frac(1, r_"orbit")) times 86400 $

$ approx 4.435 times 10^{-3} times 1.193 times 10^{-7} times 86400 approx +45.7 text(" μs/Tag") $

Das positive Vorzeichen zeigt, dass die Satellitenuhr *schneller* läuft.

#line(length: 100%)


= Kombinierte Korrektur

SR und GR wirken gleichzeitig:

$ Delta t_"net" = Delta t_"SR" + Delta t_"GR" = -7.2 + 45.7 = +38.5 text(" μs/Tag") $

Dies ist die Korrektur, die in GPS programmiert ist.

== Positionsfehler ohne Korrektur

$ Delta x = c times Delta t = 3 times 10^8 times 38.5 times 10^{-6} = 11.55 text(" km/Tag") $

Ohne die relativistische Korrektur würde GPS nach 24 Stunden um *11,5 km* abweichen.

#line(length: 100%)


= Die Nullpunkt-Höhe

Es gibt eine Höhe, wo SR und GR sich aufheben: $Delta t_"SR" + Delta t_"GR" = 0$.

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

== Sagnac-Effekt

Das Signal braucht ungefähr $70$ ms zum Empfänger. Weil sich die Erde währenddessen dreht, muss zusätzlich die Sagnac-Korrektur berücksichtigt werden:

$ Delta t_"Sagnac" = frac(bold(Omega) dot (bold(r) _"receiver" times bold(r) _"sat"), c^2) $

Für die geozentrischen Vektoren bedeutet dies das Gleiche wie $Delta t_"Sagnac" = frac(Omega, c^2) (x_"receiver" y_"sat" - y_"receiver" x_"sat")$. Die typische Größe beträgt $"pm" 100$–150 ns.

#line(length: 100%)


= Zusammenfassung

#table(
  columns: (1.5fr, 1fr, 1fr),
  [*Effekt*], [*Typ*], [*Größe*],
  [Spezielle Relativität], [Linear], [-7.2 μs/Tag],
  [Allgemeine Relativität], [Linear], [+45.7 μs/Tag],
  [Nettokorrektur (GPS)], [Linear], [+38.5 μs/Tag],
  [Exzentrizität (GPS)], [Begrenzt], [±34 ns],
  [Sagnac-Fenster], [Begrenzt], [±100–150 ns],
)

#line(length: 100%)


= Referenzen

+ Ashby, Neil. "Relativity in the Global Positioning System." *Living Reviews in Relativity* 6, no. 1 (2003).
+ GPS.gov Technical Specifications.
+ ESA Galileo User Handbook.
