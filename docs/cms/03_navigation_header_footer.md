# HolzerPrompt CMS – Navigation, Header, Footer und Sprachführung

**Version:** 0.3  
**Status:** Konzept / Grundlage für Implementierung  
**Geltungsbereich:** Globale Website-Navigation und sprachabhängige Menüführung

## 1. Grundprinzip

Header und Footer sind keine `PageBlock`-Typen.

Sie sind globale Bestandteile des Website-Layouts und werden zentral in Templates eingebunden:

```text
base.html
│
├── partials/header.html
│   └── Hauptnavigation
│
├── Seiteninhalt
│   └── PageBlocks
│
└── partials/footer.html
    └── Footer-Navigation
```

Jede Site und jede Sprache erhält ihre eigene Navigation.

## 2. Sprachabhängige Navigation

Beispiele:

```text
holzerprompt.de + de + main
holzerprompt.com + en + main
holzerprompt.com + fr + main
holzerprompt.com + es + main
```

Die Navigation wird nicht nur zur Laufzeit übersetzt, sondern als eigenständiges redaktionelles Objekt gespeichert.

Dadurch können Bezeichnungen und perspektivisch auch Menüstrukturen je Sprache angepasst werden.

## 3. Navigation

Das Modell `Navigation` wird site- und sprachfähig.

Vorgesehene Felder:

```text
site
language
identifier
name
created_at
updated_at
```

Beispiele:

```text
Site: holzerprompt.de
Language: de
Identifier: main
Name: Hauptnavigation
```

```text
Site: holzerprompt.com
Language: en
Identifier: main
Name: Main Navigation
```

Eindeutig:

```text
site + language + identifier
```

Typische Identifier:

```text
main
footer
```

Später bei Bedarf:

```text
footer_legal
footer_services
```

## 4. NavigationItem

Vorgesehene Felder:

```text
navigation
label
page
external_url
parent
position
is_visible
```

Ein Eintrag kann:

1. auf eine interne `Page` verweisen,
2. auf eine externe URL verweisen,
3. als reiner Dropdown-Öffner ohne Ziel dienen, sofern er Unterpunkte besitzt.

## 5. Interne Ziele

Interne Navigationseinträge verweisen bevorzugt auf `Page`, nicht auf eine hartcodierte URL.

Beispiel:

```text
Navigation EN
Label: Contact
Page: Kontakt
```

Das CMS löst für den aktuellen Kontext auf:

```text
Site = holzerprompt.com
Language = en
```

und verwendet die passende `PageTranslation`.

Damit können Slugs je Sprache variieren, ohne Navigationslinks manuell anzupassen.

## 6. Externe Ziele

Externe URLs bleiben möglich und gehören zum konkreten sprachabhängigen `NavigationItem`.

Ein NavigationItem darf grundsätzlich nicht gleichzeitig eine interne Page und eine externe URL als Ziel verwenden.

## 7. Untermenüs

Für die erste Version werden maximal zwei Ebenen unterstützt:

```text
Ebene 1
└── Ebene 2
```

Beispiel Deutsch:

```text
Startseite
Leistungen
├── Prozessanalyse
├── KI-Projekte
└── Website & SEO
Entwicklungspartnerprogramm
Wissen
Kontakt
```

Beispiel Englisch:

```text
Home
Services
├── Process Analysis
├── AI Solutions
└── Website & SEO
Development Partner Program
Insights
Contact
```

Keine dritte Ebene und keine Mega-Menüs in v0.3.

## 8. Validierungen

`NavigationItem` muss mindestens folgende Regeln prüfen:

- interne Page und externe URL nicht gleichzeitig
- Parent gehört zur selben Navigation
- Parent darf nicht das Element selbst sein
- Parent darf in v0.3 keinen eigenen Parent besitzen
- Position steuert die Reihenfolge
- ein ziel-loser Eintrag ist nur als sinnvoller Container/Dropdown zulässig

## 9. Navigationserzeugung für neue Sprachen

Beim Aufbau einer neuen Sprache soll perspektivisch eine bestehende Navigation als Strukturvorlage verwendet werden können.

Beispiel:

```text
[Navigation aus deutscher Version erzeugen]
```

Übernommen werden:

```text
Hierarchie
Positionen
interne Ziel-Pages
Sichtbarkeit
```

Übersetzt bzw. neu gepflegt werden:

```text
Label
eventuelle sprachabhängige Zusatztexte
externe URLs bei Bedarf
```

Die Übersetzung der Labels kann später über dasselbe CI-Machine-Übersetzungsmodul erfolgen.

## 10. Header

Der Header enthält in v0.3 zunächst:

```text
Logo / Markenname
Hauptnavigation
Mobile-Menü
später Sprachumschalter
```

Noch nicht Teil der ersten Version:

```text
Mega-Menü
Suche
Login
mehrere Header-Varianten
CMS-konfigurierbare Farben
```

Grundstruktur:

```text
<header>
    <nav aria-label="Hauptnavigation">
        ...
    </nav>
</header>
```

Bootstrap wird lokal ausgeliefert.

## 11. Mobile Navigation

Die mobile Navigation basiert zunächst auf Bootstrap Navbar/Collapse.

Anforderungen:

- gut per Touch bedienbar
- Dropdown-Untermenüs erreichbar
- korrekte `aria-*`-Attribute
- Tastaturbedienung
- keine zusätzliche JS-Bibliothek für v0.3

## 12. Aktive Menüeinträge

Die aktuelle Seite wird als aktiv markiert.

Bei aktiver Unterseite wird auch der übergeordnete Bereich erkennbar.

Beispiel:

```text
Services        ← aktiver Bereich
└── Process Analysis ← aktuelle Seite
```

Die Ermittlung soll nicht durch komplexe URL-Vergleiche im Template erfolgen, sondern über die gemeinsame `Page`-/`PageTranslation`-Struktur.

## 13. Template-Integration

Views sollen Navigationen nicht jeweils manuell laden müssen.

Bevorzugtes Konzept:

```django
{% load navigation_tags %}
{% render_navigation "main" %}
```

Der Template-Tag verwendet den bereits bestimmten Site- und Sprachkontext.

Vorgesehene Struktur:

```text
website/templates/website/
├── base.html
├── page.html
├── partials/
│   ├── header.html
│   ├── navigation.html
│   └── footer.html
└── blocks/
```

und:

```text
cms/templatetags/navigation_tags.py
```

## 14. Footer

Der Footer wird ebenfalls global über `base.html` eingebunden.

Die Footer-Navigation ist site- und sprachabhängig:

```text
holzerprompt.de + de + footer
holzerprompt.com + en + footer
holzerprompt.com + fr + footer
```

Beispiel:

```text
Impressum
Datenschutz
Kontakt
```

Weitere Footer-Spalten können später über zusätzliche Navigation-Identifier aufgebaut werden.

## 15. Sprachumschalter

Der Sprachumschalter gehört perspektivisch in den Header der internationalen Site.

Er soll auf die entsprechende Übersetzung derselben `Page` führen.

Beispiel:

```text
EN /process-analysis/
→ FR /fr/analyse-des-processus/
```

Nur veröffentlichte Sprachfassungen werden als direkte Alternative angeboten.

Die deutsche `.de`-Site kann ebenfalls als Sprachalternative verknüpft werden, obwohl sie eine andere Domain verwendet.

## 16. Fehlende Navigation

Fehlt eine Navigation für den aktuellen Site-/Sprachkontext, darf die Website nicht mit einem 500-Fehler abbrechen.

Produktionsverhalten:

```text
Navigation nicht ausgeben
```

Im DEBUG-Modus kann ein hilfreicher Hinweis vorgesehen werden.

## 17. SiteSettings – spätere Erweiterung

Logo und globale Header-/Footer-Einstellungen gehören nicht in `Navigation`.

Später kann `SiteSettings` unter anderem enthalten:

```text
Logo
Favicon
Website-Name
Standard-OG-Bild
Header-CTA
```

Sprachabhängige globale Texte müssen separat berücksichtigt werden.

Für die erste Header-Version kann der Markenname statisch im Template stehen.

## 18. Verbindliche Entscheidungen

- Header und Footer sind globale Templates, keine PageBlocks.
- Jede Site und Sprache besitzt eigene Navigationen.
- `Navigation` wird durch `site + language + identifier` bestimmt.
- Interne Menüziele verweisen auf `Page`, nicht auf feste sprachabhängige URLs.
- Maximal zwei Menüebenen in v0.3.
- Bootstrap übernimmt Navbar, Dropdown und Mobile-Grundfunktion.
- Navigation wird über einen zentralen Template-Mechanismus geladen.
- Sprachumschalter verknüpft zusammengehörige `PageTranslation`-Objekte.
- Navigationen dürfen redaktionell zwischen Sprachen abweichen.

## 19. Noch offen

- Exaktes Admin-UX für Navigationseinträge.
- Automatische/halbautomatische Übersetzung von Navigationen.
- Verhalten des Sprachumschalters bei fehlender Übersetzung.
- Finale Footer-Struktur.
- Zeitpunkt der Einführung von `SiteSettings`.
- Sticky Header ja/nein.

## 20. Umsetzungsreihenfolge

1. Multi-Site-/Language-Grundmodell fertigstellen.
2. `Navigation` um Site und Sprache erweitern.
3. `NavigationItem` validieren.
4. vorhandene Navigation migrieren.
5. `base.html` einführen.
6. `page.html` auf `base.html` umstellen.
7. Navigation-Template-Tag.
8. `header.html`.
9. Bootstrap-Hauptnavigation.
10. Dropdowns.
11. Mobile Navigation.
12. aktive Menüeinträge.
13. Footer.
14. zweite Sprache mit eigener Navigation testen.
15. Sprachumschalter.
