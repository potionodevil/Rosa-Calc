# ROSA Hardware

**Sprachmodelle mit einer Billion Parametern laufen auf einem Einzelplatz-PC rechnerisch mit 46 bis 63 Tokens pro Sekunde.**

![Status](https://img.shields.io/badge/Status-Hardware--Entwurf-orange)
![Sprache](https://img.shields.io/badge/Sprache-Deutsch-blue)
![Lizenz](https://img.shields.io/badge/Lizenz-Alle%20Rechte%20vorbehalten-lightgrey)

Hardware-Entwurf, kein Silizium, kein Prototyp. Nicht veröffentlicht. Stand 17.11.2026.

## Auf einen Blick

- Entwurf B, zusammen mit einer RTX 5090, führt ein 1T-MoE-Modell bei 32.000 Tokens Kontext rechnerisch mit 46 bis 63 Tok/s aus. Eine Workstation mit 768 GB RAM erreicht 18 Tok/s, eine RTX 5090 mit Host-RAM 1,6 Tok/s.
- Das ergibt 8,2 Antworten pro Stunde und 1.000 US-Dollar Systempreis. Die Workstation erreicht 3,9.
- Entwurf A, eigenständig betrieben, scheiterte in der unabhängigen Gegenprüfung. Er schlägt die RTX 5090 beim dichten 32B-Modell nicht.
- Nebenergebnis: Auf dem Testrechner mit RTX 3050 steigt Qwen3-30B-A3B bei 32.000 Tokens Kontext durch kostenlose Einstellungen rechnerisch auf das 2,3- bis 4-Fache.

Schreibweise: Tok/s heißt Tokens pro Sekunde. 32k heißt 32.768 Tokens Kontext. Eine Antwort heißt 32k Prompt plus 500 Ausgabetokens. Alle Werte gelten für eine Person, Batch 1, Gewichte mit 4,125 Bit.

## Problem

Beim Generieren mit Batch 1 warten die Rechenwerke auf den Speicher.

- Ein Sprachmodell rechnet beim Decoding mit Batch 1 nur 1 bis 4 FLOP pro gelesenem Byte. GPUs brauchen 117 bis 1.174 FLOP pro Byte für volle Auslastung. Sie nutzen damit 0,3 bis 3,4 % ihrer Rechenleistung.
- Die Geschwindigkeit folgt der Speicherbandbreite: Tokens pro Sekunde sind höchstens Bandbreite geteilt durch gelesene Bytes pro Token.
- Große Modelle passen nicht in den Grafikspeicher. Ein 1T-MoE-Modell belegt bei 4,125 Bit 529 GB. Die RTX 5090 hat 32 GB, die RTX PRO 6000 96 GB.
- Der Mac Studio M5 Ultra mit 512 GB kostet 22.299 US-Dollar und fasst das 1T-Modell trotzdem nicht.
- Der KV-Cache wächst mit dem Kontext. Qwen3-32B liest bei 32k pro Token 8,6 GB KV-Cache zusätzlich zu den Gewichten (berechnet aus der Modellkonfiguration).
- Eine Recherche über sieben Hardware-Klassen findet 2026 keine, die einem Einzelplatz mehr Bandbreite pro Dollar liefert als eine GPU.

## Ergebnisse

Alle Geschwindigkeiten sind berechnete Obergrenzen. Effizienz 72 % der Spitzenbandbreite für alle Geräte, kalibriert an veröffentlichten Messungen. Bei den Entwürfen steht "untere / obere Annahme" für zwei belegte Werte der Speicherbandbreite.

### Entwurf A, eigenständig: Verlauf über drei Runden

Tok/s, berechnet.

| Modell und Kontext | Runde 1, beste Variante | Runde 2, korrigiert (untere / obere Annahme) | RTX 5090 | M5 Ultra 512 GB | RTX PRO 6000 |
|---|---|---|---|---|---|
| dichtes 32B, 32k | 75,4 | 12,2 / 28,3 | 50,6 | 34,1 | 50,6 |
| gpt-oss-120b, 32k | 442 | 74,5 / 169 | 56,5 mit Host-RAM | 215 | 315 |
| TSG Standard, 4k | 53,7 | 9,2 / 21,1 | 16,0 mit Host-RAM | 36,6 | 28,7 mit Host-RAM |

- Runde 0 und 1 sahen Entwurf A auf gpt-oss-120b und TSG 3- bis 6,6-mal vor einer RTX 5090.
- Ein unabhängiges Red Team fand 18 Befunde. Die belegte dauerhafte Speicherbandbreite liegt bei 0,20 bis 0,47 TB/s statt angenommen 1,25 TB/s.
- Entwurf A bräuchte 0,85 TB/s, um die RTX 5090 beim dichten 32B-Modell einzuholen. Er ist verworfen.
- Mit Prefill dauert eine Antwort auf dem dichten 32B-Modell 400 s, auf der RTX 5090 40,6 s.

### Entwurf B, zusammen mit einer RTX 5090

Tok/s bei 32k, berechnet.

| Modell | Entwurf B (untere / obere Annahme) | RTX 5090 mit 128 GB RAM | RTX 5090 mit 768 GB, 8 Kanäle | RTX PRO 6000 96 GB | M5 Ultra 512 GB |
|---|---|---|---|---|---|
| gpt-oss-120b | 118 / 176 | 56,5 | 126 | 315 | 215 |
| 1T-MoE, Kimi-K2-Klasse | 46,2 / 63,3 | 1,59 | 18,0 | 1,88 | 3,44 |
| DeepSeek-V4.1-Flash | 56,9 / 105 | 3,86 | 34,8 | 6,38 | 102 |
| TSG Standard | 25,2 / 32,7 | 14,4 | 26,4 | 24,0 | 29,5 |
| dichtes 32B | 50,6 | 50,6 | 50,6 | 50,6 | 34,1 |

Antworten pro Stunde und 1.000 US-Dollar Systempreis (berechnet, untere Annahme):

| Modell | Entwurf B | RTX 5090 mit 128 GB RAM | Workstation 768 GB | M5 Ultra 512 GB |
|---|---|---|---|---|
| 1T-MoE | 8,2 | 2,0 | 3,9 | 0,67 |
| DeepSeek-V4.1-Flash | 13,4 | 3,7 | 6,6 | 2,9 |
| gpt-oss-120b | 52,9 | 53,8 | 27,2 | 11,0 |

- Energie pro Token beim 1T-MoE: Entwurf B 6,0 J, Workstation 27,0 J, M5 Ultra 44,7 J, RTX 5090 mit Host-RAM 285 J (berechnet).
- Preis von Entwurf B ohne GPU und Host: 3.795 US-Dollar für 128 GB bis 6.343 US-Dollar für 512 GB. Die Monte-Carlo-Spanne über die Kostenannahmen (p10 bis p90) reicht von 2.389 bis 11.062 US-Dollar.
- Systempreis mit RTX 5090 und Host: 7.574 bis 10.122 US-Dollar.
- Entwurf B gewinnt nur bei Modellen von 128 bis 512 GB. Bei gpt-oss-120b liegt er im Preis-Leistungs-Verhältnis gleichauf mit einer RTX 5090 und Host-RAM.

### Kalibrierung

| Gerät | gpt-oss-120b berechnet, 80 % Effizienz | gpt-oss-120b gemessen, veröffentlicht |
|---|---|---|
| DGX Spark | 43,0 Tok/s | 38,55 Tok/s |
| Strix Halo | 40,3 Tok/s | 34,13 Tok/s |

Das Rechenmodell lag 10 bis 15 % zu hoch. Runde 2 rechnet deshalb mit 72 % Effizienz für alle Geräte.

### Gemessen auf dem Testrechner

| Größe | Wert |
|---|---|
| GPU | RTX 3050 6 GB, 168 GB/s, PCIe 3.0 x8, 70 W |
| RAM | 31 GB DDR4-2666, 13,9 bis 18,6 GB/s mit 1 bis 8 Prozessen |
| NVMe sequenziell | 2,83 GB/s bei 1 MiB und Warteschlange 32 |
| NVMe zufällig | 63.432 IOPS bei 4 KiB, Warteschlange 32 |

### Nebenergebnis: Maßnahmen für den Testrechner

Berechnete Obergrenzen in Tok/s. Die Spalte "Rechner" nimmt DDR4-3200 an, die letzte Spalte setzt die gemessene RAM-Bandbreite ein. Preise sind Annahmen für 2026.

| Maßnahme | Kosten | Wirkung, Rechner | mit gemessenem RAM |
|---|---|---|---|
| Software-Einstellungen | 0 EUR | Qwen3-30B-A3B bei 32k: 9,4 auf 21,9 | 3,4 bis 4,5 auf 11,0 bis 13,6 |
| RAM-Module neu stecken | 0 EUR | Qwen3-30B-A3B bei 32k: 19,9 bei 42,7 GB/s | entfällt |
| gebrauchte RTX 3090 24 GB | etwa 700 EUR | dichtes 8B bei 4k: 21,6 auf 132 | gleich |
| 128 GB RAM plus Software-Einstellungen | etwa 500 EUR | gpt-oss-120b bei 4k: 0,68 auf 14,1 | 6,3 bis 8,2 |

## Grenzen

- Kein ROSA-Wert ist gemessen. Alle Geschwindigkeiten, Energien und Preise sind Rechnungen.
- Eine zentrale Komponente gibt es 2026 nur als Spezifikation. Dauerhafte Bandbreite, Energie pro Bit und Lebensdauer kann nur ein Hersteller beantworten.
- Die frühestmögliche Verfügbarkeit von Entwurf B liegt bei 2029 (Einschätzung).
- Das Rechenmodell lag auf zwei Geräten 10 bis 15 % über veröffentlichten Messungen.
- Entwurf B braucht eine GPU im System. Die Übergabezeit zwischen GPU und Entwurf B ist eine Annahme.
- Entwurf B lohnt sich nur für Modelle von 128 bis 512 GB. Modelle unter 96 GB laufen auf vorhandenen GPUs gleich gut oder besser.
- Preise beruhen auf Kostenannahmen. Die Monte-Carlo-Spanne reicht über den Faktor 4,6.
- Die Messungen am Testrechner liefen unter Fremdlast. Die Lücke zwischen 18,6 und 42,7 GB/s RAM-Bandbreite ist ungeklärt.
- Geräte von 2027 bis 2029, etwa RTX 6090 oder Medusa Halo, sind nur als Gerücht bekannt und nicht gerechnet.

## Stand und Fahrplan

| Phase | Inhalt | Stand |
|---|---|---|
| Runde 0 | Rechenmodell und erster Entwurf | abgeschlossen |
| Runde 1 | Varianten gegen den schwächsten Faktor | abgeschlossen |
| Runde 2 | Unabhängige Gegenprüfung, korrigierte Zahlen, Entwurf B | abgeschlossen |
| Phase 1 | Messungen am Testrechner: RAM neu stecken, Einstellungen mit llama-bench prüfen. Ziel: innerhalb von 30 % der Rechnung | geplant |
| Phase 2 | Nachbildung von Entwurf B in Software auf vorhandener Hardware. Ziel: innerhalb von 30 % der Rechnung | geplant |
| Phase 3 | Thermik- und Simulatorstudie | geplant |
| Phase 4 | Herstellerangaben einholen. Abbruch bei unter 0,2 TB/s oder über 2.000 US-Dollar pro Speichereinheit | geplant |
| Phase 5 | FPGA-Prototyp, nur nach Erfolg in Phase 2 bis 4 | geplant |
| Phase 6 | Marktbeobachtung. Entscheidung 2028: kaufen statt bauen | laufend |

## Projektstruktur

```
rosa-hardware/
  README.md
  MANIFEST.md
  requirements.txt
  testbett/      Testdaten, Generatoren, Bewertungsskripte
  ergebnisse/    Messwerte und Auswertungen
```

Das Repository enthält das Testbett und die Ergebnisse. Jede Datei steht mit Zweck und Größe in `MANIFEST.md`. Code und Methodik des Verfahrens sind nicht Teil dieses Repositorys.

## Zugehörige Arbeit

- Interner Forschungsbericht, November 2026, unveröffentlicht.
- Eigene Vorarbeit (2026): KI-Effizienz auf Consumer-Hardware. Unveröffentlicht.
- Verwandtes Projekt: tsg-120t liefert die Last "TSG Standard".

## Lizenz

Alle Rechte vorbehalten. Keine Nutzung ohne Zustimmung.

Kontakt: auf Anfrage
