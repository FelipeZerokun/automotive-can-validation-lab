# Learning-to-Project Map / Zuordnung von Lernstoff und Projekt

The repository grows only when the related concept has been studied. This keeps
all GitHub claims aligned with actual knowledge.

Das Repository wächst nur, wenn das zugehörige Konzept behandelt wurde. Dadurch
bleiben alle Aussagen auf GitHub mit dem tatsächlichen Kenntnisstand im Einklang.

| Status | Theory topic / Theoriethema | Project increment / Projekterweiterung |
|---|---|---|
| ✅ | CAN fundamentals / CAN-Grundlagen | Repository structure, typed application data, prepared standard frame / Repository-Struktur, typisierte Anwendungsdaten, vorbereiteter Standard-Frame |
| ✅ | Signals, scaling and offset / Signale, Skalierung und Offset | Manual encoding and decoding with tests / Manuelle Codierung und Decodierung mit Tests |
| ⬜ | Classic CAN frame structure / Aufbau des Classic-CAN-Frames | Document frame fields and distinguish application payload from protocol fields / Frame-Felder dokumentieren und Nutzdaten von Protokollfeldern unterscheiden |
| ⬜ | Standard and extended identifiers / Standard- und Extended-Identifier | Add identifier validation and comparison examples / Identifier-Prüfung und Vergleichsbeispiele ergänzen |
| ⬜ | Byte order and bit layout / Byte-Reihenfolge und Bitbelegung | Add focused endian and bit-packing exercises / Übungen zu Endianness und Bit-Packing ergänzen |
| ⬜ | DBC files / DBC-Dateien | Add DBC network definition and `cantools` encoder/decoder / DBC-Netzwerkdefinition und `cantools`-Codierung ergänzen |
| ⬜ | Data transmission with `python-can` / Datenübertragung mit `python-can` | Send and receive the prepared frame on `VirtualBus` / Vorbereiteten Frame über `VirtualBus` senden und empfangen |
| ⬜ | Cyclic and event-based messages / Zyklische und ereignisgesteuerte Nachrichten | Add ECU scenario generator and transmission scheduler / ECU-Szenariogenerator und Sendeplanung ergänzen |
| ⬜ | Cycle times and timeouts / Zykluszeiten und Timeouts | Add deterministic timing monitor and timeout tests / Deterministische Zeitüberwachung und Timeout-Tests ergänzen |
| ⬜ | Restbus simulation / Restbussimulation | Simulate missing network participants / Fehlende Netzwerkteilnehmer simulieren |
| ⬜ | Rolling counters and checksums / Botschaftszähler und Prüfsummen | Add simplified end-to-end protection checks / Vereinfachte End-to-End-Schutzprüfungen ergänzen |
| ⬜ | Error states and bus load / Fehlerzustände und Buslast | Add analysis tools and document virtual-bus limitations / Analysewerkzeuge und Einschränkungen des virtuellen Busses dokumentieren |
| ⬜ | Requirements-based validation / Anforderungsbasierte Validierung | Complete traceability matrix, reports and regression suite / Rückverfolgbarkeitsmatrix, Berichte und Regressionstests vervollständigen |

## Current definition of done / Aktuelle Definition of Done

- [x] The repository installs as a Python project. / Das Repository lässt sich als Python-Projekt installieren.
- [x] A physical vehicle state can be represented. / Ein physikalischer Fahrzeugzustand kann dargestellt werden.
- [x] The state can be encoded into a documented payload. / Der Zustand kann in dokumentierte Nutzdaten codiert werden.
- [x] The payload can be decoded again. / Die Nutzdaten können wieder decodiert werden.
- [x] Identifier and payload are prepared for future transmission. / Identifier und Nutzdaten sind für die spätere Übertragung vorbereitet.
- [x] Automated tests verify the behavior. / Automatisierte Tests verifizieren das Verhalten.
- [ ] No claim of real CAN transmission is made yet. / Es wird noch keine reale CAN-Übertragung behauptet.
