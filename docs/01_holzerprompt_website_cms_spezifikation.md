# HolzerPrompt Website & CMS – Technische Spezifikation v0.1

**Status:** Entwurf / Grundlage für die Implementierung  
**Zweck:** Spezifikation der neuen HolzerPrompt-Website einschließlich eines schlanken, eigenen Content-Management-Systems auf Django-Basis.  
**Testdomain:** `hp.dev-cim.de`  
**Produktivziel:** `holzerprompt.de`

---

## 1. Zielbild

Die HolzerPrompt-Website wird als **eigenständige Django-Anwendung** entwickelt und betrieben. Sie ist technisch und fachlich von der CI-Machine getrennt, verwendet jedoch dieselbe technologische Basis und kann über eine definierte API mit der CI-Machine kommunizieren.

Die Website übernimmt insbesondere:

- Unternehmensdarstellung und Marketing
- SEO-Inhalte und Wissensbereich
- Landingpages
- Darstellung von Leistungen und Anwendungsfällen
- Entwicklungspartnerprogramm
- Kontakt- und Lead-Einstieg
- Einbindung bzw. Ansteuerung ausgewählter CI-Machine-Module
- insbesondere später: KI-Potenzialanalyse / Process-Discovery-Wizard

Die Website selbst enthält **keine fachliche Prozesslogik der CI-Machine**.

---

## 2. Architekturprinzipien

### 2.1 Trennung von Website und CI-Machine

Die beiden Systeme bleiben eigenständig:

```text
hp.dev-cim.de
HolzerPrompt Website / Django
        │
        │ HTTPS / API
        ▼
dev-cim.de
CI-Machine / Django
```

Die Trennung gilt für:

- Quellcode
- Django-Projekt
- virtuelle Python-Umgebung
- Gunicorn-Service
- Unix-Socket bzw. Port
- Datenbank
- Deployment
- Konfiguration / Secrets
- Logging

### 2.2 Gemeinsamer Testserver

Auf dem bestehenden Testserver können beide Anwendungen parallel betrieben werden.

Empfohlene Verzeichnisstruktur:

```text
/home/jochen/
├── clean-machine/          # bestehende CI-Machine
└── holzerprompt-web/       # neue Website
```

Nginx übernimmt das Domain-Routing:

```text
dev-cim.de     -> CI-Machine
hp.dev-cim.de  -> HolzerPrompt Website
```

### 2.3 Schlankes CMS statt Universal-CMS

Das CMS soll **kein WordPress-Ersatz mit beliebig erweiterbarer Plugin-Architektur** werden.

Ziel ist ein kleines, kontrolliertes Redaktionssystem für die tatsächlichen Anforderungen von HolzerPrompt.

Grundsatz:

> Nur Funktionen entwickeln, die für die HolzerPrompt-Website konkret benötigt werden oder mit hoher Wahrscheinlichkeit wiederverwendbar sind.

---

## 3. Technologiestack

### Backend

- Python
- Django
- PostgreSQL
- Gunicorn
- Nginx

### Frontend

Initial bevorzugt:

- serverseitig gerenderte Django Templates
- HTML5
- CSS
- möglichst wenig JavaScript
- Progressive Enhancement statt SPA

Ein schweres Frontend-Framework wie React oder Vue ist für Version 1 nicht vorgesehen.

### Infrastruktur

- HTTPS über Let's Encrypt
- Cloudflare optional bzw. bevorzugt vorgeschaltet
- Git-basierter Deployment-Prozess
- getrennte Umgebungsvariablen / Secrets
- regelmäßige Datenbank- und Datei-Backups

---

## 4. Kernmodule der Website

### 4.1 Seitenverwaltung

Ein Modell `Page` verwaltet redaktionelle Seiten.

Vorgesehene Kernfelder:

- `title`
- `slug`
- `status` (`draft`, `published`)
- `parent` optional
- `template_type`
- `meta_title`
- `meta_description`
- `canonical_url` optional
- `robots_index`
- `robots_follow`
- `created_at`
- `updated_at`
- `published_at`

### 4.2 Blocksystem

Seiten sollen aus einem begrenzten Satz strukturierter Inhaltsblöcke bestehen.

Für Version 1 vorgesehen:

- Hero
- Rich Text
- Bild + Text
- Spalten / Feature Cards
- Call-to-Action
- FAQ
- Referenz / Case Study Teaser
- Formular
- CI-Machine-Modul / Wizard-Einstieg

Wichtig:

Das Blocksystem ist **kein freier Page Builder**. Layout und Design bleiben durch Templates kontrolliert.

### 4.3 Navigation

Navigation wird redaktionell pflegbar.

Benötigt werden mindestens:

- Hauptnavigation
- Footer-Navigation
- Reihenfolge
- externe Links
- interne Seitenverknüpfung
- optional Sichtbarkeitssteuerung

### 4.4 Wissensbereich / Artikel

Für SEO und fachliche Inhalte wird ein eigener Bereich vorgesehen.

Modell `Article` bzw. `KnowledgeArticle`:

- Titel
- Slug
- Teaser
- Inhalt
- Beitragsbild
- Autor optional
- Kategorie
- Tags optional
- Veröffentlichungsdatum
- SEO-Metadaten

### 4.5 Leistungen / Anwendungsfälle

Leistungen und spätere Referenzmodule sollen strukturiert gepflegt werden können.

Beispielhafte Entitäten:

- `Service`
- `UseCase`
- `Reference`

Diese müssen nicht zwingend in Version 1 vollständig umgesetzt werden, sollten aber im Datenmodell berücksichtigt werden.

---

## 5. SEO-Anforderungen

Die Website soll sämtliche grundlegenden technischen SEO-Funktionen ohne zusätzliche Plugins bereitstellen.

Pflichtfunktionen:

- individuelle `<title>`-Tags
- Meta Description
- Canonical URL
- robots meta
- XML-Sitemap
- `robots.txt`
- OpenGraph-Metadaten
- Twitter/X Cards soweit sinnvoll
- strukturierte Daten über JSON-LD
- saubere semantische HTML-Struktur
- sprechende URLs
- 301-Redirect-Verwaltung für migrierte WordPress-URLs

Für die Migration von `holzerprompt.de` müssen bestehende indexierte URLs geprüft und möglichst über Redirects erhalten werden.

---

## 6. Formulare

### 6.1 Allgemein

Kontaktformulare werden nativ in Django umgesetzt.

Anforderungen:

- CSRF-Schutz
- serverseitige Validierung
- Spam-Schutz
- Rate Limiting
- Cloudflare Turnstile bevorzugt
- E-Mail-Benachrichtigung
- optional Speicherung als Lead
- Datenschutzhinweis / Einwilligung, wo erforderlich

### 6.2 Datentrennung

Normale Website-Kontaktanfragen können zunächst in der Website-Datenbank gespeichert werden.

Daten aus CI-Machine-Prozessen wie dem Process-Discovery-Wizard sollen dagegen grundsätzlich von der CI-Machine verarbeitet und gespeichert werden.

---

## 7. Datenschutz und Consent

Die Website muss DSGVO-konform betrieben werden.

Vorgesehen:

- Consent-Lösung für nicht notwendige Dienste
- Google Analytics nur nach entsprechender Einwilligung, sofern eingesetzt
- Consent Mode soweit relevant
- Datenschutzerklärung
- Impressum
- nachvollziehbare Speicherdauern
- möglichst datensparsame Konfiguration

Die konkrete Consent-Komponente wird separat bei der Implementierung festgelegt.

---

## 8. Benutzer und Redaktion

Für Version 1 reicht die Django-Authentifizierung mit Admin-Zugang.

Rollen initial:

- Administrator
- Redakteur optional

Externe Kundenkonten sind **nicht Bestandteil des Website-CMS**.

Kundenkonten und fachliche Nutzerkonten gehören zur CI-Machine.

---

## 9. CI-Machine-Integration

Die Website kennt CI-Machine-Module nur über klar definierte Integrationspunkte.

Beispiele:

- Start eines Wizards
- Übergabe einer Website-/Mandantenkennung
- Abruf eines Ergebnisstatus
- Anzeige eines fertigen Ergebnisses
- Übergabe eines Leads

Die konkrete Schnittstelle wird im Dokument `02_ci_machine_api_spezifikation.md` beschrieben.

### Grundsatz

> Die Website darf keine interne CI-Machine-Datenbank direkt lesen oder beschreiben.

Alle systemübergreifenden Zugriffe erfolgen über eine definierte API.

---

## 10. Sicherheitsanforderungen

### Anwendung

- aktuelles Django
- keine unnötigen Pakete
- keine Upload-Ausführung
- sichere Session-Cookies
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- HSTS nach stabiler Inbetriebnahme
- Content Security Policy soweit praktikabel
- X-Content-Type-Options
- Referrer Policy

### Betrieb

- separater Unix-User optional später
- eigener Gunicorn-Service
- eigener Socket
- eigener Datenbankbenutzer
- minimale DB-Rechte
- `.env` / Secrets außerhalb des Repositories
- Fail2ban / Firewall auf Serverebene
- regelmäßige Updates
- Backups
- Logging

---

## 11. Deployment

Empfohlener Ablauf:

```text
lokale Entwicklung
    ↓
Git Repository
    ↓
Testserver hp.dev-cim.de
    ↓
Tests / Review
    ↓
später Produktion holzerprompt.de
```

Test- und Produktivkonfigurationen müssen getrennt sein.

---

## 12. Mindestumfang Version 1

Die erste produktionsfähige Version soll mindestens enthalten:

1. Basis-Django-Projekt
2. CMS-Seitenmodell
3. Blocksystem mit wenigen Kernblöcken
4. Navigation
5. SEO-Grundfunktionen
6. Kontaktformular
7. Impressum / Datenschutz
8. Wissensbereich oder vorbereitete Artikelstruktur
9. CI-Machine-Integrationskomponente
10. Deployment auf `hp.dev-cim.de`
11. Security-Grundkonfiguration
12. Backup- und Logging-Konzept

---

## 13. Explizit nicht Bestandteil von Version 1

- allgemeiner visueller Page Builder
- Plugin-Marktplatz
- Shop
- komplexe Medienverwaltung
- Mandantenfähigkeit der Website
- Benutzerportal für Kunden
- umfangreiche Workflow-Funktionen
- eigene KI-Logik innerhalb der Website

---

## 14. Offene Architekturentscheidungen vor Implementierung

Vor Programmierbeginn bzw. im ersten technischen Sprint festzulegen:

- genaue Repository-Struktur
- separates Repository vs. gemeinsamer Git-Account / Projektgruppe
- Modellierung des Blocksystems
- Medienverwaltung
- Consent-Lösung
- Rate-Limiting-Mechanismus
- API-Authentifizierung zur CI-Machine
- Logging-Ziel
- Backup-Strategie der Website-Datenbank

---

## 15. Leitentscheidung

Die Website wird als **eigenständige, schlanke Django-Website mit kleinem CMS** umgesetzt.

Sie soll stabil, sicher und wartbar sein und bewusst weniger Funktionen als ein Universal-CMS besitzen.

Die CI-Machine bleibt ein separates System. Die Integration erfolgt ausschließlich über definierte Schnittstellen.
