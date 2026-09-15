# HolzerPrompt CMS – Übersetzungsworkflow und Redaktion

**Version:** 0.3  
**Status:** Konzept / Grundlage für UI und Services  
**Geltungsbereich:** CMS-seitige Bedienung und Statusverwaltung

## 1. Ziel

Dieses Dokument beschreibt, wie Redakteure Übersetzungen im HolzerPrompt-CMS anlegen, aktualisieren, prüfen und veröffentlichen.

Die eigentliche KI-Übersetzung erfolgt in der CI-Machine. Das CMS bleibt verantwortlich für:

- Auswahl von Quelle und Zielsprachen
- Ermittlung der zu übersetzenden Inhalte
- Übersetzungsstatus
- Speicherung der Ergebnisse
- redaktionelle Prüfung
- Veröffentlichung
- Schutz manueller Änderungen

## 2. Masterprinzip

Die deutsche Sprachfassung ist zunächst die Masterquelle.

Typischer Ablauf:

```text
Deutsch bearbeiten
↓
Deutsch speichern/veröffentlichen
↓
Übersetzungen werden ggf. als veraltet markiert
↓
Übersetzung starten
↓
CI-Machine
↓
Übersetzungsentwurf
↓
Review
↓
manuelle Korrektur
↓
Veröffentlichung
```

## 3. Bedienung auf der deutschen Seite

Die zentrale Übersetzungsaktion befindet sich auf der Bearbeitungsoberfläche der deutschen Masterseite.

Beispiel:

```text
Seite: Prozessanalyse
Master: Deutsch

Übersetzungen

Sprache       Status                 Aktion
---------------------------------------------------
Englisch      aktuell                Öffnen
Französisch   nicht vorhanden        Erstellen
Spanisch      Quelle geändert        Aktualisieren
```

Mögliche Aktionen:

```text
Übersetzung erstellen
Übersetzung aktualisieren
Übersetzung öffnen
Übersetzung prüfen
Status anzeigen
```

Zusätzlich:

```text
[Fehlende/veraltete Übersetzungen erstellen]
```

## 4. Erstübersetzung

Existiert eine Zielsprachfassung noch nicht, lautet die Aktion beispielsweise:

```text
[Englische Übersetzung erstellen]
```

Dabei werden angelegt:

```text
PageTranslation
+
PageBlockTranslation für alle übersetzbaren Blöcke
```

Das Ergebnis wird zunächst nicht automatisch veröffentlicht.

Zielstatus nach erfolgreicher KI-Übersetzung:

```text
publication_status = draft
translation_status = review
```

## 5. Aktualisierung

Existiert eine Sprachfassung bereits und wurde die deutsche Quelle geändert:

```text
[Englische Übersetzung aktualisieren]
```

Die Standardaktion soll nur Inhalte aktualisieren, deren Quelle geändert wurde.

Bereits aktuelle Blöcke werden nicht neu generiert.

## 6. Übersetzungsdialog

Beim Start wird ein Dialog vorgesehen:

```text
Übersetzungen erstellen/aktualisieren

Zielsprachen:
☑ Englisch
☑ Französisch
☐ Spanisch

Umfang:
○ Ganze Seite
● Nur geänderte Inhalte

[Abbrechen] [Übersetzung starten]
```

Bei einer Erstübersetzung entspricht „ganze Seite“ dem Normalfall.

Bei Aktualisierungen ist „nur geänderte Inhalte“ die bevorzugte Standardoption.

## 7. Fachliche Einheit: Seite

Der Redakteur startet einen Übersetzungsjob auf Seitenebene.

Die Seite ist die fachliche Einheit, damit die CI-Machine den vollständigen Kontext erhält.

Technisch werden Inhalte block- und feldweise übersetzt.

Prinzip:

```text
ganze Seite = Kontext
1..n Blöcke/Felder = Übersetzungsziele
```

## 8. Änderungserkennung

Das CMS muss perspektivisch erkennen können, welche Zielinhalte gegenüber der deutschen Quelle veraltet sind.

Status auf Seitenebene:

```text
current
source_changed
```

Zusätzlich Status auf Blockebene:

```text
Hero: current
Rich Text 1: source_changed
CTA: current
```

Dadurch kann eine Seite insgesamt veröffentlicht bleiben, während einzelne Übersetzungen aktualisiert werden müssen.

## 9. Statusmodell

### Veröffentlichungsstatus

```text
draft
published
```

### Übersetzungsstatus

```text
missing
current
source_changed
translating
review
```

Bedeutung:

- `missing`: Sprachfassung existiert nicht.
- `current`: Zielinhalt entspricht dem bekannten Stand der Quelle.
- `source_changed`: Quelle wurde seit der letzten Übersetzung geändert.
- `translating`: Übersetzungsjob läuft.
- `review`: neues KI-Ergebnis liegt vor und soll redaktionell geprüft werden.

Fehlerzustände des technischen Jobs werden separat behandelt und nicht mit dem redaktionellen Status vermischt.

## 10. Übersetzungsansicht

Eine Zielsprachfassung bleibt normal editierbar.

Beispiel:

```text
Seite: Process Analysis
Sprache: Englisch
Quelle: Deutsch
Übersetzungsstatus: Prüfung erforderlich

[Deutsche Quelle anzeigen]
[Neu übersetzen]
```

Darunter befinden sich die normalen Eingabefelder der Sprachfassung.

KI-Ergebnisse sind redaktionelle Entwürfe, keine unveränderlichen Ergebnisse.

## 11. Manuelle Nachbearbeitung

Nach der KI-Übersetzung darf ein Redakteur Texte verändern.

Das CMS soll perspektivisch pro Sprachinhalt erkennen:

```text
automatisch erzeugt
manuell nachbearbeitet
```

Ein mögliches Feld:

```text
manually_edited = true/false
```

Eine robustere Revisionslogik kann später ergänzt werden.

## 12. Schutz manueller Änderungen

Eine automatische Aktualisierung darf manuell nachbearbeitete Zieltexte nicht stillschweigend überschreiben.

Bei Konflikten ist mindestens eine Warnung erforderlich:

```text
Dieser Zieltext wurde nach der letzten Übersetzung manuell bearbeitet.

[Abbrechen]
[Neue Übersetzung als Vorschlag]
[Bestehenden Text ersetzen]
```

Für v0.1 der Übersetzungsfunktion kann zunächst eine einfachere Warnung verwendet werden. Die Service-Architektur darf spätere Vorschlags-/Revisionsfunktionen nicht verhindern.

## 13. Einzelblock-Aktualisierung

Später kann an einem veralteten Block eine kleine Aktion angeboten werden:

```text
Rich Text
Status: Quelle geändert

[Neu übersetzen]
```

Dabei erhält die CI-Machine weiterhin den Seitenkontext, übersetzt aber nur den ausgewählten Block.

Die normale Hauptaktion bleibt auf Seitenebene.

## 14. Zentrale Übersetzungsübersicht

Zusätzlich zur Seitenbearbeitung wird eine Übersetzungsübersicht vorgesehen.

Beispiel:

| Seite | DE | EN | FR | ES |
|---|---|---|---|---|
| Startseite | Master | aktuell | aktuell | fehlt |
| Prozessanalyse | Master | Quelle geändert | Review | fehlt |
| Kontakt | Master | aktuell | aktuell | aktuell |

Zweck:

- fehlende Sprachfassungen erkennen
- veraltete Sprachfassungen erkennen
- Review-Bedarf erkennen
- zu Seiten/Sprachfassungen navigieren

Batch-Übersetzungen sind eine spätere Erweiterung.

## 15. Service-Schicht

Die Übersetzungslogik darf nicht direkt in `admin.py` implementiert werden.

Ziel:

```text
Admin / spätere CMS-UI
        ↓
CMS Translation Service
        ↓
CI-Machine API Client
```

Der Service übernimmt beispielsweise:

- Payload aufbauen
- übersetzbare Felder bestimmen
- Jobs starten
- Status speichern
- Ergebnisse validieren
- Ergebnisse den richtigen `PageTranslation`-/`PageBlockTranslation`-Objekten zuordnen

Damit kann die Admin-Oberfläche später ersetzt oder erweitert werden, ohne die Integrationslogik neu zu schreiben.

## 16. Fehlerbehandlung

Ein technischer Fehler darf vorhandene veröffentlichte Übersetzungen nicht beschädigen.

Grundregel:

```text
bestehende Daten bleiben erhalten
↓
neues Ergebnis vollständig validieren
↓
erst dann übernehmen
```

Fehler müssen nachvollziehbar sein, beispielsweise:

```text
Job fehlgeschlagen
Zeitpunkt
Zielsprache
betroffene Seite
technischer Fehlercode
erneut versuchen
```

## 17. Keine automatische Veröffentlichung

Eine KI-Übersetzung wird standardmäßig nicht unmittelbar veröffentlicht.

Normaler Ablauf:

```text
CI-Ergebnis
→ draft/review
→ redaktionelle Prüfung
→ publish
```

Eine spätere Option für automatisierte Veröffentlichung kann separat entschieden werden.

## 18. Verbindliche Entscheidungen

- Übersetzung wird primär auf der deutschen Seitenoberfläche gestartet.
- Zentrale Übersetzungsübersicht dient als Cockpit.
- Erstübersetzung und Aktualisierung sind getrennte Aktionen.
- Ganze Seite liefert Kontext; einzelne Blöcke/Felder sind technische Übersetzungsziele.
- Nur geänderte Inhalte können gezielt neu übersetzt werden.
- KI-Ergebnisse bleiben editierbar.
- Manuelle Änderungen werden vor automatischem Überschreiben geschützt.
- Übersetzungen werden standardmäßig als Entwurf/Review gespeichert.
- CMS-Integrationslogik liegt in einer Service-Schicht, nicht im Admin-Code.

## 19. Noch offen

- Exakte technische Änderungserkennung/Versionierung.
- Detaildesign der Admin-Oberfläche.
- Umfang der ersten Konflikt-/Revisionslogik.
- Batch-Funktionen.
- Benachrichtigungen bei abgeschlossenen Jobs.
- Rechte/Rollen für Übersetzen, Review und Veröffentlichen.

## 20. Umsetzungsreihenfolge

1. Statusfelder im Datenmodell vorbereiten.
2. deutsche Masterfassung eindeutig kennzeichnen.
3. manuelle zweite Sprache ohne KI vollständig unterstützen.
4. Übersetzungsbereich auf der Page-Admin-Oberfläche.
5. zentrale Statusübersicht.
6. CMS Translation Service.
7. CI-Machine API Client.
8. Jobstart und Statusabfrage.
9. Ergebnisübernahme.
10. Review-/Publish-Workflow.
11. gezielte Blockaktualisierung.
12. Schutz/Revision manueller Änderungen ausbauen.
