# Process-Discovery / KI-Potenzialanalyse Wizard – Vorläufige Spezifikation v0.1

**Status:** bewusst vorläufig  
**Zweck:** Rahmen für die spätere Implementierung eines öffentlichen CI-Machine-Wizards auf der HolzerPrompt-Website.  
**Wichtiger Vorbehalt:** Die fachliche Interviewlogik wird erst nach realen Testinterviews konkretisiert.

---

## 1. Ziel

Der Wizard soll Interessenten dabei helfen, **mögliche Ansatzpunkte für KI-gestützte Prozessverbesserungen im eigenen Unternehmen zu erkennen**.

Er bildet nicht das vollständige Prozessinterview ab.

Er übernimmt vielmehr dessen **erste Discovery-Phase**:

> Tätigkeiten und Abläufe sichtbar machen, erste Prozesskandidaten erkennen und entscheiden, ob eine vertiefte Analyse sinnvoll ist.

Der Wizard ist damit zugleich:

- Beratungsinstrument
- Qualifizierungsinstrument
- Demonstration der HolzerPrompt-Methode
- Lead-Einstieg
- erstes öffentliches Process-Discovery-Modul der CI-Machine

---

## 2. Bewusste Abgrenzung

Der Wizard soll zunächst **nicht**:

- einen vollständigen Geschäftsprozess modellieren
- verbindliche Automatisierungsempfehlungen geben
- Wirtschaftlichkeitsberechnungen durchführen
- technische Lösungsarchitekturen festlegen
- behaupten, eine Tätigkeit vollständig automatisieren zu können
- ein echtes vertiefendes Prozessinterview ersetzen

Sein Ziel ist ein qualifizierter nächster Schritt.

---

## 3. Forschungs- und Entwicklungsprinzip

Die erste Interviewrunde wird **nicht softwaregestützt**, sondern in realen Gesprächen durchgeführt.

Die daraus gewonnenen Erfahrungen sollen genutzt werden, um unter anderem festzustellen:

- Welche Fragen werden verstanden?
- Welche Fragen sind zu abstrakt?
- Welche Reihenfolge funktioniert?
- Wo erzählen Interviewpartner spontan relevante Details?
- Welche Nachfragen sind häufig erforderlich?
- Welche Informationen sind für die Identifikation eines Prozesskandidaten tatsächlich relevant?
- Welche Informationen lassen sich sinnvoll standardisieren?
- Wo braucht es menschliche Interpretation?

Erst danach wird die Wizard-Logik konkretisiert.

---

## 4. Was bereits festgelegt werden kann

Unabhängig von den späteren konkreten Fragen gelten folgende Strukturprinzipien.

### 4.1 Der Nutzer startet bei einer konkreten Arbeitssituation

Der Wizard soll möglichst nicht mit abstrakten Fragen beginnen wie:

> „Wo möchten Sie KI einsetzen?“

Stattdessen soll er von tatsächlichen Tätigkeiten, Arbeitsabläufen und Problemen ausgehen.

### 4.2 Prozesskandidaten statt Gesamtunternehmen

Das Ziel ist nicht, das gesamte Unternehmen zu analysieren.

Der Wizard soll einzelne Tätigkeiten bzw. Teilprozesse erkennen, die sich für eine spätere detaillierte Betrachtung eignen.

### 4.3 Schrittweise Konkretisierung

Der Nutzer wird von allgemeinem Kontext zu konkreteren Merkmalen geführt.

### 4.4 Ergebnis als Hypothese

Das Resultat ist eine erste Hypothese über mögliches Potenzial, keine abschließende Beratung.

---

## 5. Vorläufiges Phasenmodell

Das folgende Modell ist ausdrücklich **kein finaler Interviewleitfaden**.

### Phase A – Orientierung

Zweck:

- Kontext herstellen
- Nutzer erklären, was betrachtet wird
- Erwartung begrenzen

Mögliche Inhalte:

- Branche / Unternehmensbereich
- Rolle des Nutzers
- grober Tätigkeitsbereich

### Phase B – Tätigkeit / Prozesskandidat entdecken

Zweck:

Eine konkrete wiederkehrende Tätigkeit oder einen Ablauf identifizieren.

Mögliche Richtungen:

- wiederkehrende Aufgaben
- häufige Kundenanfragen
- Recherchearbeit
- Informationsübertragung
- Prüfung / Bewertung
- Text- oder Dokumentenerstellung
- manuelle Dateneingabe
- Abstimmungen

### Phase C – Tätigkeit charakterisieren

Vorläufig relevante Merkmale:

- Häufigkeit
- Zeitaufwand
- Standardisierungsgrad
- Anzahl beteiligter Personen
- Informationsquellen
- Entscheidungsanteil
- wiederkehrende Regeln
- Ausnahmefälle
- Medienbrüche
- Recherchebedarf
- Dokument-/Textanteil

Welche dieser Merkmale tatsächlich benötigt werden, wird aus den Interviews abgeleitet.

### Phase D – Potenzialsignale erkennen

Der Wizard bzw. später die CI-Machine versucht Hinweise zu erkennen, beispielsweise:

- hohe Wiederholung
- viele strukturierte Informationen
- wiederkehrende Entscheidungen
- häufige Recherche
- hoher manueller Übertragungsaufwand
- bekannte Regeln
- wiederkehrende Textproduktion
- wiederkehrende Klassifikation

Diese Liste ist vorläufig und darf nicht als finales Scoring verstanden werden.

### Phase E – Vorläufiges Ergebnis

Mögliche Ergebnisformen:

- kein klarer Prozesskandidat erkannt
- Prozesskandidat erkannt
- mehrere Prozesskandidaten erkannt
- vertiefendes Interview empfohlen

Das Ergebnis sollte nachvollziehbar begründet werden.

### Phase F – Optionaler Kontakt / nächster Schritt

Der Nutzer kann anschließend:

- Ergebnis ansehen
- weitere Informationen zu HolzerPrompt erhalten
- Kontakt aufnehmen
- ein vertiefendes Prozessinterview anfragen

---

## 6. Vorläufiges Datenmodell

Das technische Datenmodell muss flexibel genug sein, damit Fragen nach den Testinterviews geändert werden können.

Vorgesehen:

### `DiscoverySession`

- UUID
- Status
- Startzeit
- letzte Aktivität
- aktuelle Phase / Schritt
- Quelle / Entry Point
- Locale
- optional Tenant / Client

### `DiscoveryAnswer`

- Session
- Frage-ID
- Antwortwert
- Datentyp
- Timestamp

### `DiscoveryResult`

- Session
- Status
- Zusammenfassung
- Ergebnisstruktur als JSON oder normalisierte Modelle
- Analyseversion
- erstellt am

### `ProcessCandidate`

Später optional:

- Titel
- Beschreibung
- erkannte Signale
- Potenzialstufe
- Begründung
- empfohlener nächster Schritt

Das Modell soll erst nach den Praxistests finalisiert werden.

---

## 7. Wizard-Engine

Die Engine sollte Fragen nicht hart in Views oder Templates codieren.

Empfohlen ist eine konfigurierbare Struktur.

Beispiel:

```python
Step(
    id="frequency",
    type="single_choice",
    question="Wie häufig tritt diese Tätigkeit auf?",
    required=True,
    options=[...],
)
```

Später möglich:

- bedingte Verzweigungen
- Folgefragen
- Überspringen irrelevanter Fragen
- Abbruchkriterien
- Zwischenauswertung

---

## 8. Abbruch- und Verzweigungslogik

Noch nicht fachlich festlegen.

Die Engine muss jedoch technisch unterstützen:

- normalen nächsten Schritt
- bedingten nächsten Schritt
- Wiederholung / Korrektur
- freiwilligen Abbruch
- fachlichen Abbruch
- Abschluss

Beispiel:

```text
Antwort
  ↓
Regelprüfung
  ├── nächste Frage
  ├── alternative Frage
  ├── Teilbereich überspringen
  └── Ergebnis erzeugen
```

---

## 9. KI-Einsatz

Der KI-Anteil ist noch nicht final festgelegt.

Denkbare Aufgaben der KI:

- Freitextantworten strukturieren
- Begriffe vereinheitlichen
- Tätigkeit zusammenfassen
- mögliche Prozesskandidaten erkennen
- Signale kategorisieren
- Ergebnis verständlich formulieren

Wichtig:

Die KI soll nicht die gesamte Interviewsteuerung unkontrolliert übernehmen.

Empfohlenes Prinzip:

> Deterministische Wizard-Struktur + gezielter KI-Einsatz an klar definierten Stellen.

---

## 10. Scoring

Für Version 0.1 wird **kein finales numerisches Scoring definiert**.

Die realen Interviews sollen zunächst zeigen, welche Merkmale überhaupt zuverlässig zwischen geeigneten und ungeeigneten Prozesskandidaten unterscheiden.

Später mögliche Dimensionen:

- Wiederholungsgrad
- Standardisierbarkeit
- Informationsstruktur
- Entscheidungslogik
- KI-Eignung
- Integrationsaufwand
- wirtschaftliches Potenzial

Die Dimensionen und Gewichtungen werden erst nach Auswertung der Interviewrunde festgelegt.

---

## 11. Ergebnisdarstellung

Das Ergebnis soll:

- verständlich
- vorsichtig formuliert
- nachvollziehbar
- handlungsorientiert

sein.

Beispielhafte Struktur:

```text
Ihre Analyse

Wir haben in Ihren Angaben einen möglichen Prozesskandidaten erkannt:

[Prozess / Tätigkeit]

Warum dieser Bereich interessant sein könnte:
- ...
- ...
- ...

Empfohlener nächster Schritt:
Vertiefende Prozessanalyse
```

Keine übertriebenen Aussagen wie:

- „Dieser Prozess kann zu 87 % automatisiert werden.“
- „Sie sparen garantiert 20 Stunden pro Monat.“

solange keine belastbare methodische Grundlage dafür existiert.

---

## 12. UX-Prinzipien

Der Wizard soll:

- kurze Schritte verwenden
- möglichst eine Fragestellung pro Screen behandeln
- Fortschritt transparent machen
- früh erklären, warum Fragen gestellt werden
- keine unnötigen Fachbegriffe verwenden
- jederzeit Zurück-Navigation erlauben
- Zwischenspeicherung über Session ermöglichen
- auf Mobilgeräten funktionieren

---

## 13. Datenschutz

Empfohlenes Prinzip:

### Phase 1

Wizard zunächst anonym / pseudonym durchführen.

### Phase 2

Kontaktdaten nur optional am Ende erfassen.

Dadurch werden fachliche Antworten nicht unnötig früh mit personenbezogenen Daten verbunden.

Vor Produktivbetrieb festzulegen:

- Speicherdauer
- Löschung nicht abgeschlossener Sessions
- Einwilligungstext
- Datenschutzhinweis
- Umgang mit sensiblen Unternehmensinformationen

---

## 14. Integration in HolzerPrompt.de

Geplante Darstellung:

```text
HolzerPrompt Landingpage
        ↓
"KI-Potenzial prüfen"
        ↓
Website startet Discovery-Session über CI-Machine API
        ↓
Wizard-UI auf HolzerPrompt-Seite
        ↓
CI-Machine steuert fachliche Session
        ↓
Ergebnis
        ↓
optional Kontakt / vertiefendes Interview
```

Die fachliche Wizard-Logik verbleibt in der CI-Machine.

---

## 15. MVP nach Abschluss der Interviewtests

Nach Auswertung der realen Interviews soll aus diesem Dokument eine Spezifikation v1.0 entstehen.

Diese soll mindestens festlegen:

1. Zielgruppe des Wizards
2. genaue Phasen
3. genaue Fragen
4. Antworttypen
5. Reihenfolge
6. Verzweigungen
7. Abbruchkriterien
8. relevante Potenzialsignale
9. KI-Einsatzpunkte
10. Ergebnislogik
11. Lead-Übergabe
12. Datenschutz
13. Testfälle

Erst danach sollte die vollständige fachliche Implementierung beginnen.

---

## 16. Was schon vorher programmiert werden kann

Unabhängig vom endgültigen Interviewdesign können bereits entwickelt werden:

- generische Sessionverwaltung
- generische Schritt-/Fragenstruktur
- flexible Antworttypen
- API-Basis
- Fortschrittsanzeige
- Zurück-/Weiter-Mechanik
- konfigurierbare Verzweigungen
- Ergebniscontainer
- Logging
- Tests der technischen Engine

Nicht vorziehen sollte man:

- konkretes Scoring
- endgültige Fragen
- finale Promptlogik
- endgültige Ergebnisbewertung

---

## 17. Forschungsprotokoll für die realen Interviews

Damit die Interviews später systematisch in die Softwareentwicklung einfließen können, sollten pro Testinterview mindestens folgende Beobachtungen dokumentiert werden:

- Welche Fragen funktionierten gut?
- Wo musste nachgefragt werden?
- Welche Begriffe waren missverständlich?
- Welche Informationen kamen ungefragt?
- Welche Informationen fehlten zunächst?
- Welche Tätigkeit wurde als Prozesskandidat ausgewählt?
- Warum wurde sie ausgewählt?
- Welche Merkmale waren für die Auswahl entscheidend?
- Welche Fragen waren überflüssig?
- Welche neue Frage ergab sich aus dem Gespräch?

Diese Auswertung bildet die Grundlage der Version 1.0.

---

## 18. Leitentscheidung

Der Wizard wird als **Process-Discovery-Modul der CI-Machine** entwickelt und über die HolzerPrompt-Website zugänglich gemacht.

Die technische Engine kann früh vorbereitet werden. Die konkrete Interviewlogik wird jedoch bewusst erst nach praktischen Interviews festgelegt.

Damit verhindert HolzerPrompt, dass ein theoretisch entworfener Fragebogen vorschnell in Software gegossen wird, bevor klar ist, welche Informationen in realen Gesprächen tatsächlich relevant sind.
