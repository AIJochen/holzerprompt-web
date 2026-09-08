# HolzerPrompt ↔ CI-Machine API – Technische Spezifikation v0.1

**Status:** Vorläufige technische Spezifikation  
**Zweck:** Definition der Schnittstelle zwischen der HolzerPrompt-Website und der separat betriebenen CI-Machine.  
**Website Testsystem:** `https://hp.dev-cim.de`  
**CI-Machine Testsystem:** `https://dev-cim.de`

---

## 1. Ziel

Die API verbindet zwei eigenständige Django-Systeme:

```text
HolzerPrompt Website
hp.dev-cim.de
        │
        │ HTTPS / JSON API
        ▼
CI-Machine
dev-cim.de
```

Sie soll zunächst vor allem den geplanten Process-Discovery-/KI-Potenzialanalyse-Wizard unterstützen.

Die Schnittstelle soll jedoch allgemein genug gestaltet werden, damit später weitere öffentliche CI-Machine-Module eingebunden werden können.

---

## 2. Grundprinzipien

### 2.1 Klare Systemgrenzen

Die Website darf niemals direkt auf:

- CI-Machine-Datenbank
- interne Django-Modelle
- interne Sessions
- Dateisystem der CI-Machine

zugreifen.

Kommunikation erfolgt ausschließlich über eine veröffentlichte API.

### 2.2 API-first für öffentliche Module

CI-Machine-Module, die extern eingebunden werden sollen, erhalten einen definierten öffentlichen API-Layer.

Die interne Fachlogik bleibt hinter diesem Layer verborgen.

### 2.3 Versionierung

API-Endpunkte werden versioniert.

Beispiel:

```text
/api/v1/public/...
```

Breaking Changes führen später zu `/api/v2/`.

---

## 3. Kommunikationsmodell

Für Version 1 wird eine JSON-basierte REST-ähnliche HTTPS-API empfohlen.

Technik:

- HTTPS ausschließlich
- UTF-8
- JSON Request/Response
- HTTP Status Codes
- CSRF nicht als primärer API-Schutz
- serverseitige API-Authentifizierung

---

## 4. Authentifizierung zwischen Website und CI-Machine

Die Website ist ein vertrauenswürdiger Server-Client.

Empfohlene erste Variante:

- eigener API-Client in der CI-Machine
- Client-ID
- serverseitig gespeichertes Secret oder signierte Requests
- Secret ausschließlich als Umgebungsvariable

Nicht vorgesehen:

- API-Key im Browser
- Secret im HTML/JavaScript
- direkter Browserzugriff auf privilegierte Endpunkte

Für Version 1 kann eine einfache, robuste Server-to-Server-Authentifizierung eingesetzt werden. Eine spätere Umstellung auf OAuth2 ist möglich, falls mehrere externe Systeme oder feinere Berechtigungsmodelle erforderlich werden.

---

## 5. Mandanten- und Herkunftskontext

Jeder Request der Website an ein öffentliches CI-Machine-Modul muss eindeutig einem Integrationsclient zugeordnet werden können.

Beispiel:

```json
{
  "client": "holzerprompt_web",
  "module": "process_discovery",
  "context": {
    "source": "hp.dev-cim.de"
  }
}
```

Später kann zusätzlich eine Tenant-ID oder Project-ID verwendet werden.

---

## 6. Process-Discovery API – vorläufiger Ablauf

Der genaue Wizard ist noch nicht final definiert. Die API sollte deshalb **nicht auf konkrete Fragen fest verdrahtet** werden.

Empfohlener Ablauf:

### 6.1 Session starten

```http
POST /api/v1/public/process-discovery/sessions/
```

Beispiel Request:

```json
{
  "client": "holzerprompt_web",
  "entry_point": "ai-potential-analysis",
  "locale": "de-DE"
}
```

Beispiel Response:

```json
{
  "session_id": "uuid",
  "status": "in_progress",
  "current_step": "welcome",
  "expires_at": "2026-09-08T18:00:00Z"
}
```

### 6.2 Aktuellen Schritt abrufen

```http
GET /api/v1/public/process-discovery/sessions/{session_id}/step/
```

Beispiel Response:

```json
{
  "step_id": "work_context",
  "type": "question_group",
  "title": "Ihr Arbeitsbereich",
  "questions": [
    {
      "id": "q_001",
      "type": "text",
      "label": "Welche wiederkehrende Tätigkeit möchten Sie betrachten?",
      "required": true
    }
  ]
}
```

### 6.3 Antworten übermitteln

```http
POST /api/v1/public/process-discovery/sessions/{session_id}/answers/
```

Beispiel:

```json
{
  "step_id": "work_context",
  "answers": {
    "q_001": "Bearbeitung eingehender Kundenanfragen"
  }
}
```

Response:

```json
{
  "accepted": true,
  "next_step": "frequency"
}
```

### 6.4 Ergebnis anfordern / abrufen

```http
POST /api/v1/public/process-discovery/sessions/{session_id}/complete/
```

Mögliche Response:

```json
{
  "status": "completed",
  "result_id": "uuid"
}
```

Anschließend:

```http
GET /api/v1/public/process-discovery/results/{result_id}/
```

---

## 7. Ergebnisstruktur – vorläufig

Da das Interview erst praktisch erprobt wird, soll das Ergebnisformat zunächst bewusst abstrakt bleiben.

Beispiel:

```json
{
  "result_id": "uuid",
  "summary": "...",
  "process_candidates": [
    {
      "title": "...",
      "potential_level": "medium",
      "signals": [
        "high_repetition",
        "structured_information",
        "manual_research"
      ],
      "next_step_recommended": true
    }
  ],
  "overall_recommendation": "deeper_interview"
}
```

Noch **nicht festschreiben**:

- konkrete Scores
- endgültige Kriterien
- Gewichtungen
- Anzahl der Prozesskandidaten
- konkrete KI-Empfehlungslogik

Diese Punkte werden erst nach den realen Interviewtests definiert.

---

## 8. Lead-Übergabe

Nach Abschluss des Wizards kann der Nutzer optional Kontaktdaten hinterlassen.

Grundsatz:

Kontaktdaten und fachliche Wizard-Daten sollten über eine definierte CI-Machine-Funktion zusammengeführt werden können.

Möglicher Endpunkt:

```http
POST /api/v1/public/process-discovery/sessions/{session_id}/lead/
```

Beispiel:

```json
{
  "name": "Max Mustermann",
  "email": "max@example.org",
  "company": "Muster GmbH",
  "consent": true
}
```

Datenschutzrechtliche Pflichttexte und konkrete Einwilligungen werden vor Implementierung festgelegt.

---

## 9. Fehlerbehandlung

Einheitliches Fehlerformat:

```json
{
  "error": {
    "code": "invalid_answer",
    "message": "Die Antwort konnte nicht verarbeitet werden.",
    "field": "q_001"
  }
}
```

Relevante Statuscodes:

- `200 OK`
- `201 Created`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`
- `409 Conflict`
- `422 Unprocessable Entity` optional
- `429 Too Many Requests`
- `500 Internal Server Error`

Keine internen Stacktraces oder technischen Details an den Client ausgeben.

---

## 10. Sicherheit

Pflichtanforderungen:

- ausschließlich HTTPS
- Rate Limiting
- API-Client-Authentifizierung
- Eingabevalidierung
- Größenlimits für Textfelder und Requests
- Schutz vor automatisiertem Missbrauch
- Logging sicherheitsrelevanter Ereignisse
- keine Secrets in Responses
- keine internen Datenbank-IDs, sofern nicht erforderlich
- bevorzugt UUIDs für öffentliche Ressourcen

Für öffentliche Wizard-Einstiege kann zusätzlich Turnstile oder ein vergleichbarer Mechanismus eingesetzt werden.

---

## 11. Datenschutz

Die API soll datensparsam arbeiten.

Zu definieren:

- Speicherdauer nicht abgeschlossener Sessions
- Speicherdauer abgeschlossener Analysen
- Trennung anonymer Wizard-Daten und personenbezogener Lead-Daten
- Löschkonzept
- Protokollierung von Einwilligungen
- Zugriff auf personenbezogene Daten

Empfehlung:

Anonyme bzw. pseudonyme Wizard-Session zunächst ohne Kontaktdaten führen. Kontaktdaten erst am Ende optional erfassen.

---

## 12. CORS und Browserzugriffe

Bevorzugte Architektur Version 1:

```text
Browser
  ↓
HolzerPrompt Django Backend
  ↓
CI-Machine API
```

Dadurch bleiben API-Secrets serverseitig.

Direkte Browserzugriffe auf privilegierte CI-Machine-Endpunkte werden vermieden.

Falls später bestimmte Endpunkte direkt aus dem Browser angesprochen werden sollen, muss CORS explizit auf freigegebene Origins begrenzt werden.

---

## 13. Logging und Nachvollziehbarkeit

Jeder API-Request sollte korrelierbar sein.

Empfohlen:

- Request-ID
- Client-ID
- Modul
- Session-ID
- Timestamp
- HTTP Status
- Laufzeit

Personenbezogene Inhalte sollen nicht unnötig in technische Logs geschrieben werden.

---

## 14. API-Abstraktion in der HolzerPrompt-Website

Die Website erhält einen eigenen Service-Layer, beispielsweise:

```text
holzerprompt_web/
└── integrations/
    └── ci_machine/
        ├── client.py
        ├── exceptions.py
        └── services.py
```

Templates und Views sollen die CI-Machine nicht direkt per HTTP ansprechen.

Dadurch kann die API später geändert oder erweitert werden, ohne die gesamte Website anzupassen.

---

## 15. API-Abstraktion in der CI-Machine

Empfohlen:

```text
ci_machine/
└── public_api/
    ├── urls.py
    ├── auth.py
    ├── serializers.py
    └── views.py

process_discovery/
├── services.py
├── models.py
└── domain/
```

Der API-Layer ruft fachliche Services auf. Fachlogik gehört nicht direkt in die API-Views.

---

## 16. Testanforderungen

Mindestens erforderlich:

- API-Authentifizierung
- Session-Erstellung
- valide Antwort
- ungültige Antwort
- abgelaufene Session
- unbekannte Session
- Rate-Limit
- Ergebniszugriff
- Lead-Übergabe
- Fehlerbehandlung

Zusätzlich Integrationstest Website → CI-Machine auf dem Testserver.

---

## 17. Nicht Bestandteil von Version 1

- externe Entwickler-API
- öffentliche API-Dokumentation für Dritte
- OAuth2 für Endkunden
- Webhooks
- Echtzeit-WebSockets
- generisches Plugin-System
- direkte Datenbankkopplung

---

## 18. Vor Implementierungsbeginn zu entscheiden

- Authentifizierungsverfahren Server-to-Server
- Session-Lebensdauer
- Rate Limits
- genaue CORS-Policy
- genaue Endpunktnamen
- DRF vs. schlanke Django-JSON-Views
- Serialisierungs-/Validierungsbibliothek
- Logging- und Monitoring-Mechanismus

---

## 19. Leitentscheidung

Die API bildet eine **stabile technische Grenze** zwischen HolzerPrompt-Website und CI-Machine.

Die Website kennt nur die veröffentlichte Schnittstelle. Die CI-Machine behält die vollständige Kontrolle über Prozesslogik, Sessionsteuerung, Analyse und Lead-Verarbeitung.

Die API soll bereits stabil genug für die Implementierung sein, aber die fachliche Struktur des Process-Discovery-Wizards bewusst noch nicht vorwegnehmen.
