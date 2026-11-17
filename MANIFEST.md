# Manifest: Ergebnisse zu bestehender Hardware

Alle geteilten Dateien. Freigegeben sind Ergebnisse zu heute erhältlicher Hardware: Roofline-Werte und die Tabelle der Sofortmaßnahmen am Referenz-PC.

| Pfad | Zweck | Herkunft | Größe (Bytes) |
|---|---|---|---|
| `.gitignore` | schließt Caches und Ausgaben aus | neu erstellt | 140 |
| `requirements.txt` | Python-Pakete des Plot-Skripts | neu erstellt | 28 |
| `testbett/roofline_plot.py` | zeichnet die Roofline der fünf Geräte aus roofline.csv und druckt die Tabelle | neu geschrieben | 2.763 |
| `ergebnisse/roofline.csv` | Bandbreite und Spitzenleistung von RTX 5090, M5 Ultra, DGX Spark, Strix Halo, RTX 3050 | aus der Prototyp-Tabelle übernommen | 221 |
| `ergebnisse/roofline_bestehende_hardware.png` | Diagramm: Roofline der fünf Geräte mit dem Batch-1-Decode-Punkt | erzeugt mit roofline_plot.py | 106.971 |
| `ergebnisse/bestehende_hardware.md` | Roofline-Tabelle, Sofortmaßnahmen am Referenz-PC, Nachmessung des Arbeitsspeichers | neu geschrieben aus den Prototyp-Tabellen | 5.648 |
| `MANIFEST.md` | diese Liste | neu erstellt | - |

Summe der aufgeführten Dateien: 115.771 Bytes (0,12 MB). `README.md` und `assets/` werden getrennt gepflegt und sind hier nicht aufgeführt.

## Voraussetzungen

- Python 3.10+, `pip install -r requirements.txt`
- Aufruf aus `testbett/`: `python roofline_plot.py` (schreibt out/roofline.png)

## Nicht enthalten

- Rechenmodell und Beschreibung des vorgeschlagenen Designs
- Varianten, Kosten-, Energie- und Sensitivitätsrechnungen zum Design
- Diagramme, die das Design zeigen
- Register, Messprotokolle und Entwurfsnotizen
