# Bestehende Hardware: Roofline bei Batch 1 und Sofortmaßnahmen am Referenz-PC

Batch-1-Decoding mit 4-Bit-Gewichten nutzt 1,1 bis 5,8 % der Spitzenrechenleistung heutiger GPUs und Unified-Memory-Rechner. Die Speicherbandbreite begrenzt, nicht die Rechenleistung. Am Referenz-PC (RTX 3050 6 GB) heben zwei kostenlose Software-Einstellungen Qwen3-30B-A3B bei 32k Kontext von 9,4 auf 21,9 Tokens/s (Modellrechnung).

Stand 17.11.2026. Alle Tokens/s sind Obergrenzen für Batch-1-Decoding bei 80 % der Spitzenbandbreite.

## 1. Roofline bei Batch 1

Batch-1-Decoding mit 4-Bit-Gewichten rechnet 2 FLOP pro Gewicht auf 0,516 Bytes (4 Bit plus ein fp16-Skalenfaktor pro 128 Gewichte): 3,88 FLOP/B.

| Gerät | Bandbreite GB/s | Spitze TFLOPS (Decode-Rechnung) | Knickpunkt FLOP/B | genutzter Anteil der Spitze bei 3,88 FLOP/B |
|---|---|---|---|---|
| RTX 5090 (FP16, FP32-Akkumulation) | 1.792 | 209,5 | 117 (FP4: 935) | 3,3 % (FP4-Pfad: 0,4 %) |
| M5 Ultra 512 GB | 1.200 | 80 (Annahme) | 67 | 5,8 % |
| DGX Spark | 273 | 100 (Annahme) | 366 | 1,1 % |
| Strix Halo | 256 | 59 (Annahme) | 230 | 1,7 % |
| RTX 3050 6 GB | 168 | 13 | 77 | 5,0 % |

GPUs lassen beim Decoding 94 bis 99 % ihrer Recheneinheiten ungenutzt. Daten: `roofline.csv`. Diagramm: `roofline_bestehende_hardware.png`, erzeugt mit `testbett/roofline_plot.py`.

## 2. Sofortmaßnahmen am Referenz-PC

Referenz-PC: RTX 3050 6 GB (168 GB/s, PCIe 3.0 x8), AM4-Plattform mit DDR4, 1-TB-NVMe (2,83 GB/s bei 1 MiB QD32, 63.432 IOPS bei 4 KiB QD32). Gewichte Q4_K_M (4,85 Bit). Obergrenzen mit 80 % der Spitzenbandbreite plus 25 µs fester Kosten pro Schicht für Kernel-Starts und Synchronisation (Annahme). Euro-Preise sind Straßenpreis-Annahmen 2026, keine Angebote.

Spalten: d8 = dichtes 8B-Modell (Llama-3.1-8B-Konfiguration), moe30 = Qwen3-30B-A3B, moe120 = gpt-oss-120b; @4k und @32k = Kontextlänge in Tokens.

| Rang | Maßnahme | EUR 2026 (Annahme) | d8@4k | d8@32k | moe30@4k | moe30@32k | moe120@4k | größter Gewinn | Tokens/s pro 100 EUR | Hinweis |
|---|---|---|---|---|---|---|---|---|---|---|
| | Ausgangslage (Schichtaufteilung, Kontext-Cache f16, 2 DIMMs DDR4-3200, mmap) | 0 | 21,6 | 7,35 | 21,0 | 9,36 | 0,681 | | | |
| 1 | Kontext-Cache q8_0 + Platzierung (Attention, Cache und häufige Experten auf der GPU) | 0 | 24,7 | 11,5 | 30,4 | 21,9 | 1,49 | moe30@32k +12,5 | kostenlos | Software |
| 2 | Kontext-Cache q4_0 (braucht Flash Attention) | 0 | 26,8 | 16,1 | 23,9 | 13,2 | 0,706 | d8@32k +8,7 | kostenlos | Qualitätsrisiko beim Abruf über lange Kontexte |
| 3 | Experten-Platzierung (llama.cpp -ot exps=CPU, KTransformers) | 0 | 21,6 | 7,47 | 29,0 | 17,1 | 1,49 | moe30@4k +8,0 | kostenlos | Software |
| 4 | Kontext-Cache q8_0 (llama.cpp -ctk/-ctv q8_0) | 0 | 24,7 | 11,4 | 22,8 | 12,8 | 0,697 | d8@32k +4,0 | kostenlos | Software-Schalter |
| 5 | explizite 1-GiB-Hugepages (+3 % CPU-Bandbreite, Annahme) | 0 | 21,7 | 7,51 | 21,5 | 9,61 | 0,683 | moe30@4k +0,5 | kostenlos | THP bereits aktiv |
| 6 | io_uring-O_DIRECT-Lader für Experten von der SSD | 0 | 21,6 | 7,35 | 21,0 | 9,36 | 1,02 | moe120@4k +0,3 | kostenlos | braucht Arbeit an der Engine |
| 7 | GPU-Tausch: gebrauchte RTX 3090 24 GB (936 GB/s) | 700 (600 bis 850) | 132 | 79,3 | 239 | 126 | 1,17 | moe30@4k +217,7 | 31,1 | Preis-Annahme; 350 W, Netzteil prüfen |
| 8 | GPU-Tausch: Klasse RTX 5060 Ti 16 GB (448 GB/s) | 470 (430 bis 520) | 66,7 | 39,2 | 51,6 | 19,6 | 0,888 | d8@4k +45,1 | 9,6 | Preis-Annahme; 180 W |
| 9 | 128 GB RAM + Platzierung + Kontext-Cache q8_0 | 500 (360 bis 720) | 24,3 | 10,3 | 27,0 | 19,9 | 14,1 | moe120@4k +13,4 | 2,7 | kombiniert |
| 10 | 4 x 32 GB DDR4 (128 GB, läuft als DDR4-2667) | 500 (360 bis 720) | 20,7 | 6,43 | 17,9 | 7,95 | 10,8 | moe120@4k +10,1 | 2,0 | bremst Modelle, die in 24 GB passen |
| 11 | zweite 1-TB-NVMe, RAID0 | 110 (80 bis 140) | 21,6 | 7,35 | 21,0 | 9,36 | 1,81 | moe120@4k +1,1 | 1,0 | nur solange Experten von der SSD kommen |
| 12 | 2 x 32 GB DDR4-3200 (64 GB, 2 DIMMs) | 250 (180 bis 360) | 21,6 | 7,35 | 21,0 | 9,36 | 2,45 | moe120@4k +1,8 | 0,7 | behält DDR4-3200 |

- Zuerst und kostenlos: Kontext-Cache q8_0 plus Experten auf der CPU (llama.cpp `-ctk q8_0 -ctv q8_0`, `-ot exps=CPU` oder KTransformers). Qwen3-30B-A3B bei 32k steigt von 9,4 auf 21,9 Tokens/s, das dichte 8B-Modell bei 32k von 7,4 auf 11,5.
- Beste bezahlte Maßnahme pro Euro für Modelle bis 24 GB: GPU-Tausch. Eine gebrauchte RTX 3090 (Annahme 700 EUR) hebt das 8B-Modell bei 4k von 21,6 auf 132 Tokens/s.
- Beste bezahlte Maßnahme für gpt-oss-120b: 4 x 32 GB DDR4 (Annahme 500 EUR) hebt es von 0,68 auf 10,8 Tokens/s, mit Kontext-Cache q8_0 und Experten-Platzierung auf 14,1. Modelle, die schon in 24 GB passen, werden um 15 % langsamer (DDR4-2667 mit 4 Dual-Rank-DIMMs).

## 3. Nachmessung des Arbeitsspeichers

Die Tabelle in Abschnitt 2 nimmt 2 x 16 GB DDR4-3200 an (51,2 GB/s Spitze). Die Nachmessung ergab drei DIMMs (8 + 8 + 16 GB DDR4-2666) und 12 bis 20 GB/s Lesebandbreite unter Fremdlast. Mit diesen Werten, freier GPU und 24 GB RAM für Gewichte gilt:

| Zustand | Maßnahme | d8@4k | d8@32k | moe30@4k | moe30@32k |
|---|---|---|---|---|---|
| DIMMs wie heute | Ausgangslage | 17,2 | 3,8 | 10,1 | 4,4 |
| DIMMs wie heute | Kontext-Cache q8_0 + Experten auf der CPU | 22,2 | 6,7 | 16,8 | 13,3 |
| DIMMs neu gesteckt (16 GB pro Kanal) | Ausgangslage | 20,7 | 6,4 | 17,9 | 8,0 |
| DIMMs neu gesteckt (16 GB pro Kanal) | Kontext-Cache q8_0 + Experten auf der CPU | 24,3 | 10,3 | 27,0 | 19,9 |

Mit beiden kostenlosen Maßnahmen und neu gesteckten DIMMs steigt Qwen3-30B-A3B bei 32k von 4,4 auf 19,9 Tokens/s, das 8B-Modell bei 32k von 3,8 auf 10,3.
