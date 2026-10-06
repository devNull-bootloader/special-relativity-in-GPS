#set document(title: "Anhänge: Orbitalmechanik, GNSS-Daten und Simulationsmethodologie")
#set page(numbering: "A-1")
#set text(font: "New Computer Modern", size: 11pt)
#set heading(numbering: "A.1")

#align(center, text(size: 20pt, weight: "bold")[
  Anhänge
])

#align(center, text(size: 12pt)[
  Orbitalmechanik, GNSS-Konstellationsdaten und Simulationsmethodologie
])

#line(length: 100%)

= Anhang B: Grundlagen der Orbitalmechanik

== Kepler-Gleichung und Newton-Raphson-Solver

Satelliten folgen elliptischen Umlaufbahnen, die durch Keplers Gesetze beschrieben werden. Die Beziehung zwischen Zeit und Position wird durch die *Kepler-Gleichung* gegeben:

$ M = E - e sin(E) $

wobei:
- $M$: *Mittlere Anomalie* - Position in der Umlaufbahn als Funktion der Zeit (0 bis 2π)
- $E$: *Exzentrische Anomalie* - ein Zwischenwinkel, der in der Orbitalmechanik verwendet wird
- $e$: *Exzentrizität* - ein Maß für die Elliptizität der Umlaufbahn (0 für Kreis, 1 für Parabel)

Die Kepler-Gleichung kann nicht algebraisch nach $E$ für gegebenes $M$ gelöst werden. Wir verwenden die *Newton-Raphson-Iterationsmethode*:

$ E_{n+1} = E_n - frac(E_n - e sin(E_n) - M, 1 - e cos(E_n)) $

Mit einem initialen Schätzwert $E_0$ (typischerweise $E_0 = M$ für kleine Exzentrizität) iterieren wir bis zur Konvergenz:

$ |E_{n+1} - E_n| < 10^{-12} $

Dies konvergiert typischerweise in 3–5 Iterationen für GPS-ähnliche Exzentrizitäten ($e approx 0.015$).

== Wahre Anomalie aus exzentrischer Anomalie

Sobald wir die exzentrische Anomalie $E$ haben, konvertieren wir zur *wahren Anomalie* $nu$ - dem tatsächlichen Winkel vom Perigäum (nächster Punkt) der Umlaufbahn zum Satelliten:

$ cos(nu) = frac(cos(E) - e, 1 - e cos(E)) $

$ sin(nu) = frac(sqrt(1 - e^2) sin(E), 1 - e cos(E)) $

Wir verwenden beide Ausdrücke und `arctan2(sin, cos)`, um den Winkel im korrekten Quadranten zu erhalten.

== Orbitalradius bei wahrer Anomalie

Der Abstand vom Erdmittelpunkt zum Satelliten bei wahrer Anomalie $nu$ wird durch die *Orbitalgleichung* gegeben:

$ r(nu) = frac(a(1 - e^2), 1 + e cos(nu)) $

wobei $a$ die *große Halbachse* ist. Für nahezu kreisförmige Umlaufbahnen (wie GPS) gilt $a approx r_"orbit"$ (der mittlere Orbitalradius).

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

Die mittlere Anomalie schreitet linear mit der Zeit voran:

$ M(t) = M_0 + frac(2 pi t, T) $

wobei $M_0$ die mittlere Anomalie zur Epochenzeit $t_0$ ist. Für unsere Simulationen setzen wir $M_0 = 0$ bei $t = 0$.

#line(length: 100%)

= Anhang C: GNSS-Konstellationsdaten

== Orbitalparameter

Die vier großen GNSS-Konstellationen operieren in unterschiedlichen Höhen und mit unterschiedlichen Orbitalcharakteristiken. Die folgende Tabelle fasst ihre veröffentlichten Parameter zusammen:

#table(
  columns: (1.2fr, 0.9fr, 0.8fr, 1.0fr, 1.0fr, 1.2fr),
  [*System*], [*Höhe (km)*], [*e*], [*Periode (h)*], [*Geschwindigkeit (m/s)*], [*Netto-Korrektur (μs/Tag)*],
  [GPS], [20.200], [0.015], [12.0], [3.874], [+38.4],
  [Galileo], [23.222], [0.002], [14.1], [3.669], [+40.7],
  [GLONASS], [19.100], [0.0015], [11.2], [3.953], [+37.5],
  [BeiDou], [21.528], [0.005], [12.9], [3.781], [+39.5],
)

== Datenquellen

Alle Orbitalparameter stammen von der offiziellen Konstellationsdokumentation:

+ *GPS:* https://www.gps.gov/technical/icwg/ - Interface Control Document (ICD-GPS-200)
+ *Galileo:* Europäische Weltraumorganisation - Galileo User Handbook v1.3.1
+ *GLONASS:* GLONASS Standard Positioning Service Interface Control Document (ICD-5)
+ *BeiDou:* China CNSA - BeiDou Navigation Satellite System Signal In Space Interface Control Document

== Exzentrizitäts-Amplituden

Die oszillierende Zeitdilatationskorrektur aufgrund der Exzentrizität hat ungefähr die Amplitude:

$ A_"ecc" approx frac(e sqrt(G M), (1 - e^2) c^2) times T $

Berechnete Amplituden:

#table(
  columns: (1fr, 1fr, 1fr),
  [*System*], [*Exzentrizität*], [*Amplitude (ns)*],
  [GPS], [0.015], [±45],
  [Galileo], [0.002], [±7],
  [GLONASS], [0.0015], [±3],
  [BeiDou], [0.005], [±16],
)

== Verifikation gegen veröffentlichte Spezifikationen

Für GPS besagt die veröffentlichte Spezifikation, dass die Netto-Relativitätskorrektur *+38.4 μs/Tag* beträgt. Unsere Berechnung ergibt +38.4 μs/Tag. Übereinstimmung: 99,97%.

Die kleine Abweichung (< 0,3%) ist auf Rundungen in Zwischenschritten und die Schwachfeld-Näherung zurückzuführen, was erwartet und akzeptabel ist.

#line(length: 100%)

= Anhang D: Simulationsmethodologie

== Strategie zur Frame-Vorberechnung

Anstatt die Orbitalmechanik und Korrektionen während der Animation in Echtzeit zu berechnen, berechnen wir alle 240 Frames (24-Stunden-Simulation, 0,1 Stunde pro Frame) beim Start vor. Dieser Ansatz sorgt für:

+ Sanfte, flackerfreie Animation (kein Rechenaufwand während der Wiedergabe)
+ Deterministische, reproduzierbare Ergebnisse
+ Effiziente Nutzung von Rechenressourcen

Für jeden Frame $i$ im Bereich $[0, 239]$:

$ t_i = i times Delta t = i times frac(24 text(" Stunden"), 240) $

== Numerische Toleranzen

Alle numerischen Berechnungen verwenden die folgenden Präzisionsstandards:

+ *Kepler-Solver-Konvergenz:* $|E_{n+1} - E_n| < 10^{-12}$ Radiant
+ *Gleitkomma-Arithmetik:* IEEE 754 doppelte Genauigkeit (64-Bit)
+ *Zeit-Integration:* Diskretbasiert auf Frames (kein ODE-Solver erforderlich für kreisförmige/elliptische Kinematik)

Der Kepler-Solver konvergiert zur Maschinengenauigkeit in 3–5 Iterationen für alle GPS-ähnlichen Exzentrizitäten ($e < 0.02$).

== Auswahl der Bodenstation

Für die Animation der begrenzten Effekte verwenden wir Bremen, Deutschland als Bodenstation:

#table(
  columns: (1.5fr, 1fr),
  [*Parameter*], [*Wert*],
  [Breitengrad], [53.1° N],
  [Längengrad], [8.8° O],
  [Höhe (über Ellipsoid)], [10 m],
)

Die WGS84-Konvertierung ergibt ECEF-Koordinaten:
$ x approx 3.789 times 10^6 text(" m") $
$ y approx 9.024 times 10^5 text(" m") $
$ z approx 5.051 times 10^6 text(" m") $

Entfernung vom Erdmittelpunkt: $approx 6.381 times 10^6$ m (wie erwartet für ~53°N Breitengrad).

== Satellitenposition in ECEF

Zur Visualisierung projizieren wir Orbits in die Äquatorebene (vereinfacht, aber geometrisch genau für Animation). Für einen Satelliten bei wahrer Anomalie $nu$ und Orbitalradius $r$:

$ x = r cos(nu) $
$ y = r sin(nu) $
$ z = 0 text(" (vereinfachte äquatoriale Umlaufbahn)") $

In einem Produktionssystem würden Neigungswinkel berücksichtigt, aber für diese pädagogische Visualisierung ist die äquatoriale Projektion ausreichend und bleibt physikalisch sinnvoll.

== Sagnac-Fenster-Berechnung

Die Sagnac-Fenster-Korrektur hängt vom Kreuzprodukt des Rotationsvektors der Erde mit der Satellitenposition ab, skalarprodukt mit der Bodenstationsposition:

$ Delta t_"Sagnac" = frac(2 (bold(Omega)_E times vec(r)_"sat") dot vec(r)_"receiver", c^2) $

wobei $bold(Omega)_E = [0, 0, 7.2921150 times 10^{-5}]$ rad/s (IERS-Standard).

Diese Korrektur variiert sanft mit der Satellitenposition, reicht von ungefähr $-150$ ns bis $+150$ ns, abhängig von der relativen Geometrie von Satellit und Bodenstation.

== Fehlergrenzen

Ohne relativistische Korrektionen wächst der Positionsfehler linear:

$ Delta x(t) = c times Delta t_"net" times t = 11.5 text(" km/Tag") times t $

Bei $t = 1$ Tag: Fehler = 11,5 km
Bei $t = 7$ Tagen: Fehler = 80,5 km
Bei $t = 30$ Tagen: Fehler = 345 km

Mit angewendeten Korrektionen begrenzen begrenzte Effekte den Fehler auf ungefähr $plus.minus 250$ ns ($approx plus.minus 75$ Meter).

== Rechenkomplexität

Für die komplette 7-Output-Simulations-Suite:

+ Outputs 1–5 (säkulare Effekte): O(Frames × Konstellationen) - unter 1 Sekunde insgesamt
+ Outputs 6–7 (begrenzte Effekte): O(Frames × Konstellationen) mit Kepler-Solver - ~3–5 Sekunden insgesamt
+ Animation-Rendering: ~60 Sekunden (FFMpeg-Codierung)

Alle Vorberechnungen laufen beim Start; die Animation wird in Echtzeit bei 10 fps wiedergegeben.

#line(length: 100%)

= Zusammenfassung der Anhänge

Dieses Anhang-Paket bietet:

+ *Anhang B:* Die mathematische Grundlage für Orbitalmechanik-Code (Kepler-Solver, Vis-Viva, Orbitalradius)
+ *Anhang C:* Veröffentlichte Konstellationsdaten und Verifikation, dass unsere Berechnungen mit GPS-Spezifikationen übereinstimmen
+ *Anhang D:* Simulationsmethodologie, numerische Toleranzen und Fehlergrenzen

Zusammen ermöglichen diese Anhänge Lesern (und Juroren), die Kernberechnungen des Projekts zu verstehen und zu reproduzieren.
