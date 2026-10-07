#set document(title: "Anhänge: Orbitalmechanik, GNSS-Daten und Simulationsmethoden")
#set page(numbering: "1")
#set text(font: "New Computer Modern", size: 11pt, lang: "de")
#set heading(numbering: none)

#align(center, text(size: 20pt, weight: "bold")[
  Anhänge
])

#align(center, text(size: 12pt)[
  Orbitalmechanik, GNSS-Konstellationsdaten und Simulationsmethoden
])

#outline(title: [Inhaltsverzeichnis], depth: 2, indent: 1em)

#line(length: 100%)

= Anhang B: Grundlagen der Orbitalmechanik

== Kepler-Gleichung und Newton-Raphson-Solver

Satelliten folgen elliptischen Umlaufbahnen, die durch Keplers Gesetze beschrieben werden. Die Beziehung zwischen Zeit und Position wird durch die *Kepler-Gleichung* gegeben:

$ M = E - e sin(E) $

wobei:
- $M$: *Mittlere Anomalie* - Position in der Umlaufbahn als Funktion der Zeit (0 bis 2π)
- $E$: *Exzentrische Anomalie* - ein Zwischenwinkel, der in der Orbitalmechanik verwendet wird
- $e$: *Exzentrizität* - ein Maß für die Elliptizität der Umlaufbahn (0 für Kreis, 1 für Parabel)

Die Kepler-Gleichung kann nicht algebraisch nach $E$ für gegebenes $M$ gelöst werden. Man verwendet die *Newton-Raphson-Iterationsmethode*:

$ E_(n+1) = E_n - frac(E_n - e sin(E_n) - M, 1 - e cos(E_n)) $

Mit einem Anfangsschätzwert $E_0$ (typischerweise $E_0 = M$ für kleine Exzentrizität) iterieren wir bis zur Konvergenz:

$ |E_(n+1) - E_n| < 10^(-12) $

Dies konvergiert typischerweise in 3–5 Iterationen für GPS-ähnliche Exzentrizitäten ($e approx 0.015$).

== Wahre Anomalie aus exzentrischer Anomalie

Sobald wir die exzentrische Anomalie $E$ haben, wandelt man zur *wahren Anomalie* $nu$ um. Das ist der eigentliche Winkel vom Perigäum (nächster Punkt) der Umlaufbahn zum Satelliten:

$ cos(nu) = frac(cos(E) - e, 1 - e cos(E)) $

$ sin(nu) = frac(sqrt(1 - e^2) sin(E), 1 - e cos(E)) $

Wir verwenden beide Ausdrücke und `arctan2(sin, cos)`, um den Winkel im korrekten Quadranten zu erhalten.

== Orbitalradius bei wahrer Anomalie

Der Abstand vom Erdmittelpunkt zum Satelliten bei wahrer Anomalie $nu$ wird durch die *Orbitalgleichung* gegeben:

$ r(nu) = frac(a(1 - e^2), 1 + e cos(nu)) $

wobei $a$ die *große Halbachse* ist. Für fast kreisförmige Umlaufbahnen (wie GPS) gilt $a approx r_"orbit"$ (der mittlere Orbitalradius).

Minimaler Abstand (Perigäum): $r_"perigee" = a(1 - e)$
Maximaler Abstand (Apogäum): $r_"apogee" = a(1 + e)$

== Orbitalgeschwindigkeit (Vis-Viva-Gleichung)

Die Geschwindigkeit des Satelliten an einem beliebigen Punkt in der Umlaufbahn wird durch die *Vis-Viva-Gleichung* gegeben:

$ v(nu) = sqrt(G M (frac(2, r(nu)) - frac(1, a))) $

Im Perigäum (nächster Punkt, $r = a(1 - e)$): Geschwindigkeit ist maximal
Im Apogäum (fernster Punkt, $r = a(1 + e)$): Geschwindigkeit ist minimal

Für GPS gibt die Näherung für kreisförmige Umlaufbahnen $v_"circ" = sqrt(G M / r) approx 3874$ m/s.

== Orbitalperiode

Die Zeit für eine vollständige Umlaufbahn ist:

$ T = 2 pi sqrt(frac(a^3, G M)) $

Dies ist *Keplers drittes Gesetz*. Für GPS ($a approx 26.57 times 10^6$ m):

$ T approx 43200 text(" s") approx 12 text(" Stunden") $

== Mittlere Anomalie aus Zeit

Die mittlere Anomalie ändert sich proportional zur Zeit:

$ M(t) = M_0 + frac(2 pi t, T) $

wobei $M_0$ die mittlere Anomalie zur Epochenzeit $t_0$ ist. Für die Simulationen setzt man $M_0 = 0$ bei $t = 0$.

#line(length: 100%)

= Anhang C: GNSS-Konstellationsdaten

== Orbitalparameter

Die vier GNSS-Systeme sind in unterschiedlichen Höhen und auf verschiedenen Umlaufbahnen. Die folgende Tabelle enthält die Modellparameter dieser Simulation. Sie ist keine Auswertung eines bestimmten Broadcast-Ephemeriden-Tages.

#table(
  columns: (1.2fr, 0.9fr, 0.8fr, 1.0fr, 1.0fr, 1.2fr),
  [*System*], [*Höhe (km)*], [*e*], [*Periode (h)*], [*Geschwindigkeit (m/s)*], [*Gesamtkorrektur (μs/Tag)*],
  [GPS], [20.200], [0.015], [12.0], [3.874], [+38.5],
  [Galileo], [23.222], [0.000394], [14.1], [3.669], [+40.7],
  [GLONASS], [19.100], [0.0015], [11.2], [3.953], [+37.5],
  [BeiDou], [21.528], [0.006801], [12.9], [3.781], [+39.5],
)

== Datenquellen und Verifikationsstatus

Die Eccentricitäten für Galileo und BeiDou wurden gegen vier offene DLR-MGEX-Broadcastdateien im RINEX-4-Format geprüft: `brd40650.25p` bis `brd40680.25p` (6.–9. März 2025). Die Dateien stammen aus dem offenen Datensatz https://doi.org/10.5281/zenodo.15110885 und enthalten täglich zusammengeführte Broadcast-Ephemeriden.

Für eine reproduzierbare Prüfung ist der IGS Multi-GNSS Pilot Project (MGEX) Broadcast-Ephemeris-Datensatz zu verwenden. IGS beschreibt das Produkt *BRD400DLR* als zusammengeführtes RINEX-4-Produkt für GPS, GLONASS, Galileo und BeiDou: https://igs.org/mgex/mgex-product-descriptions/. Die tägliche Datei enthält je Satellit und Epoche die Broadcast-Orbitparameter; für diese Prüfung ist das Feld $e$ (Eccentricity) auszulesen. Ein bestimmter IGS-Dateiname, Tag und Satellit müssen im Ergebnis angegeben werden.

Die aus diesen Dateien ausgelesenen Bereiche sind $0.0000298 <= e_"Galileo" <= 0.0007732$ und $0.0001015 <= e_"BeiDou" <= 0.0134956$. Für die Einwert-Simulationen verwenden wir die jeweiligen Stichprobenmediane $e_"Galileo" = 0.000394$ und $e_"BeiDou" = 0.006801$. BeiDou umfasst dabei verschiedene Orbitalfamilien; der Median ist daher nur ein Repräsentationswert, keine universelle Konstellationskonstante.

== Exzentrizitäts-Amplituden

Die oszillierende Zeitdilatationskorrektur aufgrund der Exzentrizität hat in erster Ordnung die Amplitude:

$ A_"ecc" approx frac(2 e sqrt(G M a), c^2) $

$ A_"ecc" = frac(e, pi) frac(v_"circ"^2, c^2) T $

Dabei ist $a$ die große Halbachse, $v_"circ" = sqrt(G M / a)$ und
$T = 2 pi sqrt(a^3 / (G M))$. Beide Formen haben die Dimension einer Zeit:
$sqrt(G M a) / c^2$ ist eine Zeit. Der Faktor $1 / pi$ ist erforderlich, wenn
die Amplitude mit $v_"circ"^2 T$ ausgedrückt wird.

Berechnete Amplituden:

#table(
  columns: (1fr, 1fr, 1fr),
  [*System*], [*Exzentrizität*], [*Amplitude (ns)*],
  [GPS], [0.015], [±34],
  [Galileo], [0.000394], [±0.95],
  [GLONASS], [0.0015], [±3.4],
  [BeiDou], [0.006801], [±15.9],
)

== Vergleich mit Ashby (2003)

Ashby berichtet in *Relativity in the Global Positioning System* (Living Reviews in Relativity 6, 1 (2003), DOI: 10.12942/lrr-2003-1) keine universelle veröffentlichte Gesamtkorrektur. Die Zahl 38,5 μs/Tag ist hier die Rundung unserer eigenen Rechnung: $-7.20 + 45.66 = 38.46$ μs/Tag.

Für den periodischen Effekt zitiert Ashby: "For a satellite of eccentricity $e = 0.01$, the maximum size of this term is about 23 ns." Für einen unabhängigen Test mit dem NTS-2-Satelliten nennt er eine gemessene Frequenzabweichung von "+442.5 parts in 10^12" gegenüber einer Vorhersage der Allgemeinen Relativität von "+446.5 parts in 10^12". Diese Werte sind keine Quelle für eine Prozentübereinstimmung unserer vereinfachten Tagesrechnung.

Quelle: https://doi.org/10.12942/lrr-2003-1 (Abschnitte "Relativistic Effects on Satellite Clocks" und "The eccentricity correction").

#line(length: 100%)

= Anhang D: Simulationsmethodologie

== Strategie zur Frame-Vorberechnung

Anstatt die Orbitalmechanik und Korrektionen während der Animation in Echtzeit zu berechnen, berechnet man alle 240 Frames (24-Stunden-Simulation, 0,1 Stunde pro Frame) beim Start vor. Die Erde dreht sich dabei genau einmal in 24 Stunden. Dieser Ansatz sorgt für:

+ Sanfte, flackerfreie Animation (kein Rechenaufwand während der Wiedergabe)
+ Reproduzierbare Ergebnisse
+ Effiziente Nutzung von Ressourcen, da die Berechnungen einmalig durchgeführt werden

Für jeden Frame $i$ im Bereich $[0, 239]$:

$ t_i = i times Delta t = i times frac(24 text(" Stunden"), 240) $

== Numerische Toleranzen

Alle numerischen Berechnungen verwenden die folgenden Genauigkeitsvorgaben:

+ *Kepler-Solver-Konvergenz:* $|E_(n+1) - E_n| < 10^(-12)$ Radiant
+ *Gleitkomma-Arithmetik:* IEEE 754 doppelte Genauigkeit (64-Bit)
+ *Zeitberechnung:* Frame-weise in festen Schritten (kein komplexer Gleichungslöser für Kreis- oder Ellipsenbahnen nötig)

Der Kepler-Solver konvergiert bis zur Genauigkeitsgrenze der Maschine in 3–5 Iterationen für alle GPS-ähnlichen Exzentrizitäten ($e < 0.02$).

== Auswahl der Bodenstation

Für die Animation der begrenzten Effekte verwenden wir Bremen (in Deutschland) als Bodenstation:

#table(
  columns: (1.5fr, 1fr),
  [*Parameter*], [*Wert*],
  [Breitengrad], [53.1° N],
  [Längengrad], [8.8° O],
  [Höhe (über Ellipsoid)], [10 m],
)

Die WGS84-Umwandlung ergibt ECEF-Koordinaten:
$ x approx 3.793 times 10^6 text(" m") $
$ y approx 0.587 times 10^6 text(" m") $
$ z approx 5.077 times 10^6 text(" m") $

Entfernung vom Erdmittelpunkt: $approx 6.365 times 10^6$ m (wie erwartet für ~53°N Breitengrad).

== Satellitenposition in ECEF

Zur Visualisierung projizieren wir Orbits in die Äquatorebene (vereinfacht, aber geometrisch genau für Animation). Für einen Satelliten bei wahrer Anomalie $nu$ und Orbitalradius $r$:

$ x = r cos(nu) $
$ y = r sin(nu) $
$ z = 0 text(" (vereinfachte äquatoriale Umlaufbahn)") $

Für diese Visualisierung wird die Bahn weiterhin als äquatorial dargestellt; die realen GNSS-Bahnneigungen von ungefähr 55–65° werden nicht simuliert. Für die Sagnac-Berechnung wird die inertiale Satellitenphase jedoch um den Erdrotationswinkel in das vereinfachte ECEF-Modell gedreht. Bremen wird in der inertialen Darstellung mit der Erde mitgedreht.

== Sagnac-Fenster-Berechnung

Die Sagnac-Fenster-Korrektur basiert auf dem Kreuzprodukt aus dem Rotationsvektor der Erde und der Satellitenposition im ECEF, welches skalar mit dem Positionsvektor des Empfängers im selben ECEF-System multipliziert wird:

$ Delta t_"Sagnac" = frac((bold(Omega)_E times vec(r)_"sat") dot vec(r)_"receiver", c^2) $

wobei $bold(Omega)_E = [0, 0, 7.2921150 times 10^(-5)]$ rad/s (IERS-Standard).

Diese Korrektur ändert sich leicht mit der Satellitenposition, reicht von ungefähr $-150$ ns bis $+150$ ns, abhängig von der relativen Geometrie von Satellit und Bodenstation.

== Fehlergrenzen

Ohne relativistische Korrektionen wächst der Positionsfehler linear:

$ Delta x(t) = c times Delta t_"net" times t = 11.5 text(" km/Tag") times t $

Bei $t = 1$ Tag: Fehler = 11,5 km
Bei $t = 7$ Tagen: Fehler = 80,5 km
Bei $t = 30$ Tagen: Fehler = 345 km

Mit angewendeten Korrektionen begrenzen begrenzte Effekte den Fehler auf ungefähr $plus.minus 250$ ns ($approx plus.minus 75$ Meter).

== Rechenkomplexität

Für die komplette 7-Output-Simulationsanhang:

+ Outputs 1–5 (lineare Effekte): $O("Frames" times "Konstellationen")$
+ Outputs 6–7 (begrenzte Effekte): $O("Frames" times "Konstellationen")$ mit Kepler-Solver
+ Animation-Rendering: abhängig von Hardware, FFmpeg-Version, Auflösung und Bitrate; keine Laufzeitmessung liegt vor.

Alle Vorberechnungen laufen beim Start; die Animation wird in Echtzeit bei 10 fps wiedergegeben.

#line(length: 100%)

= Zusammenfassung der Anhänge

Dieses Dokument enthält:

+ *Anhang B:* Die mathematische Grundlage für Orbitalmechanik-Code (Kepler-Solver, Vis-Viva, Orbitalradius)
+ *Anhang C:* Modellparameter, Quellenstatus und geplante Prüfung gegen IGS-Broadcast-Ephemeriden
+ *Anhang D:* Simulationsmethoden, numerische Toleranzen und Fehlergrenzen
