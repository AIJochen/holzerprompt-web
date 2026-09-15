# HolzerPrompt CMS – Multi-Site und Mehrsprachigkeit

**Version:** 0.3  
**Status:** Konzept / Grundlage für die Implementierung  
**Geltungsbereich:** HolzerPrompt Website-CMS

## 1. Ziel

Das HolzerPrompt-CMS wird als gemeinsame Django-Anwendung für mehrere Sites und mehrere Sprachen aufgebaut.

Geplantes Zielbild:

```text
holzerprompt.de
└── Deutsch
    └── führende Master-Inhalte

holzerprompt.com
├── Englisch
├── Französisch
├── Spanisch
└── weitere Sprachen
```

Die deutsche Website ist die inhaltliche Ausgangsbasis. Internationale Sprachfassungen werden daraus abgeleitet, sind nach ihrer Erzeugung aber eigenständig redaktionell bearbeitbare und veröffentlichbare Inhalte.

Es werden **keine getrennten CMS-Installationen pro Domain oder Sprache** betrieben.

## 2. Architekturprinzipien

Das CMS trennt:

1. Site
2. Sprache
3. sprachunabhängige Inhaltsidentität
4. sprachabhängige Inhaltsfassung
5. sprachunabhängige Blockstruktur und Darstellung
6. sprachabhängige Blockinhalte
7. Veröffentlichung
8. Übersetzungsstatus

Das CMS enthält keine eigene LLM- oder Promptlogik. KI-gestützte Übersetzungen werden später über die CI-Machine ausgeführt.

## 3. Site

Es wird ein Modell `Site` eingeführt.

Vorgesehene Kernfelder:

```text
name
domain
is_active
created_at
updated_at
```

Beispiele:

```text
HolzerPrompt Deutschland
holzerprompt.de
```

```text
HolzerPrompt International
holzerprompt.com
```

Die konkrete Entwicklungsdomain darf von der Produktionsdomain abweichen. Das Datenmodell darf nicht von genau einer Domain ausgehen.

## 4. Language

Sprachen werden zentral über `Language` verwaltet.

Vorgesehene Felder:

```text
code
name
native_name
is_active
```

Beispiele:

```text
de | Deutsch      | Deutsch
en | Englisch     | English
fr | Französisch  | Français
es | Spanisch     | Español
```

Die Sprachcodes orientieren sich an geeigneten standardisierten Sprachkennungen.

## 5. SiteLanguage

Nicht jede Sprache muss auf jeder Site verfügbar sein. Die Zuordnung erfolgt über `SiteLanguage`.

Vorgesehene Felder:

```text
site
language
is_default
is_active
url_prefix
position
```

Beispiel:

```text
holzerprompt.de
└── de | default | prefix ""

holzerprompt.com
├── en | default | prefix ""
├── fr |         | prefix "fr"
└── es |         | prefix "es"
```

Pro Site darf nur eine aktive Standardsprache definiert sein.

## 6. URL-Strategie

### Deutschland

```text
https://holzerprompt.de/
https://holzerprompt.de/leistungen/
https://holzerprompt.de/kontakt/
```

Die Standardsprache Deutsch erhält kein `/de/`-Präfix.

### International

Englisch ist zunächst Standardsprache:

```text
https://holzerprompt.com/
https://holzerprompt.com/services/
https://holzerprompt.com/contact/
```

Weitere Sprachen erhalten ein Präfix:

```text
https://holzerprompt.com/fr/
https://holzerprompt.com/fr/analyse-des-processus/
https://holzerprompt.com/es/
```

Slugs sind sprachabhängig.

## 7. Page als sprachunabhängige Inhaltsidentität

`Page` repräsentiert künftig die gemeinsame fachliche Seite und nicht mehr eine konkrete Sprachfassung.

Vorgesehene Aufgaben von `Page`:

```text
interne Identität
Parent/Seitenhierarchie
Template-Typ
Erstellungs-/Änderungsdaten
```

Optional kann ein `internal_name` zur eindeutigen redaktionellen Identifikation verwendet werden.

Die gemeinsame `Page` ersetzt die Notwendigkeit eines separaten `translation_key`: Alle `PageTranslation`-Objekte derselben `Page` gehören logisch zusammen.

## 8. PageTranslation

Die konkrete veröffentlichbare Sprachfassung liegt in `PageTranslation`.

Vorgesehene Felder:

```text
page
site
language
title
slug
status
meta_title
meta_description
canonical_url
robots_index
robots_follow
published_at
created_at
updated_at
translation_status
```

Beispiel:

```text
Page: Prozessanalyse
Site: holzerprompt.de
Language: de
Title: Prozessanalyse
Slug: prozessanalyse
Status: published
```

```text
Page: Prozessanalyse
Site: holzerprompt.com
Language: en
Title: Process Analysis
Slug: process-analysis
Status: published
```

Die Kombination aus Page, Site und Sprache darf nur einmal vorkommen.

Slug-Eindeutigkeit ist innerhalb des jeweiligen Site-/Sprach-/Parent-Kontexts sicherzustellen.

## 9. Veröffentlichung und Übersetzungsstatus

Veröffentlichung und Übersetzungszustand werden getrennt behandelt.

### Veröffentlichungsstatus

```text
draft
published
```

### Übersetzungsstatus

Mindestens:

```text
missing
current
source_changed
translating
review
```

Die deutsche Masterfassung benötigt fachlich keinen normalen Übersetzungsstatus und wird in der Oberfläche als `Master` gekennzeichnet.

Eine veröffentlichte Übersetzung darf den Status `source_changed` besitzen: Sie bleibt sichtbar, obwohl die deutsche Quelle inzwischen geändert wurde.

## 10. PageBlock

Die Blockstruktur wird gemeinsam von allen Sprachfassungen einer `Page` verwendet.

Beispiel:

```text
Page
├── Block 10: Hero
├── Block 20: Rich Text
├── Block 30: Features
└── Block 40: CTA
```

`PageBlock` enthält nur sprachunabhängige Struktur- und Darstellungsdaten, z. B.:

```text
page
block_type
position
media
is_active
variant
image_position
image_width
image_height
image_fit
zusätzliche CSS-Klassen
HTML-ID
```

Die konkrete Speicherung blocktypspezifischer Layoutwerte kann weiterhin in einem kontrollierten JSON-Feld erfolgen.

## 11. PageBlockTranslation

Sprachabhängige Blockinhalte werden in `PageBlockTranslation` gespeichert.

Vorgesehene Kernfelder:

```text
page_block
site
language
data
translation_status
manually_edited
created_at
updated_at
```

Beispiel Hero DE:

```json
{
  "headline": "KI-Potenziale erkennen",
  "text": "Wir analysieren Ihre Geschäftsprozesse.",
  "button_label": "Mehr erfahren"
}
```

Beispiel Hero EN:

```json
{
  "headline": "Identify AI potential",
  "text": "We analyse your business processes.",
  "button_label": "Learn more"
}
```

Die Kombination aus PageBlock, Site und Sprache darf nur einmal vorkommen.

## 12. Übersetzbare und strukturelle Felder

Jeder Blocktyp definiert explizit seine übersetzbaren Felder.

### Hero

Übersetzbar:

```text
headline
text
button_label
```

Strukturell:

```text
variant
image_position
image_width
image_height
image_fit
```

### Rich Text

Übersetzbar:

```text
heading
lead
content
```

Strukturell:

```text
variant
text_width
alignment
```

Diese Definition ist die Grundlage für Admin-Formulare und die spätere CI-Machine-Übergabe.

## 13. Interne Links

Interne Ziele sollen perspektivisch nicht als hartcodierte sprachspezifische URL gespeichert werden.

Bevorzugtes Prinzip:

```text
target_page = Kontakt
```

Das CMS löst daraus die passende `PageTranslation` für Site und Sprache auf.

Beispiel:

```text
DE → /kontakt/
EN → /contact/
FR → /fr/contact/
```

Externe URLs bleiben möglich.

Für freie Rich-Text-Links ist später ein gesondertes Konzept erforderlich.

## 14. MediaAsset und MediaAssetTranslation

Das eigentliche Medium bleibt sprachunabhängig.

`MediaAsset`:

```text
file
media_type
width
height
copyright_notice
created_at
updated_at
```

Sprachabhängige Metadaten wandern perspektivisch nach `MediaAssetTranslation`:

```text
media_asset
language
title
alt_text
caption
```

Dasselbe Bild kann damit je Sprache korrekte Alt-Texte und Beschriftungen erhalten.

## 15. KnowledgeArticle

Für Wissensinhalte gilt dasselbe Prinzip:

```text
KnowledgeArticle
└── KnowledgeArticleTranslation
```

Das Basisobjekt beschreibt die gemeinsame Inhaltsidentität. Titel, Slug, Text, SEO-Daten und Veröffentlichungsstatus liegen in der Sprachfassung.

## 16. Redirects

Redirects müssen mindestens sitebezogen sein:

```text
site
old_path
new_path / target
is_active
```

Damit können gleiche Pfade auf unterschiedlichen Domains unabhängig behandelt werden.

## 17. SEO

SEO-Daten werden pro Sprachfassung gepflegt.

Dazu gehören:

```text
Meta Title
Meta Description
Canonical
Robots Index
Robots Follow
```

Später erzeugt das CMS aus zusammengehörigen `PageTranslation`-Objekten die passenden `hreflang`-Verweise einschließlich eines bewusst definierten `x-default`.

Sitemaps berücksichtigen Site, Sprache und Veröffentlichungsstatus.

## 18. Sprachumschalter

Der Sprachumschalter soll möglichst zur entsprechenden Übersetzung derselben `Page` führen.

Beispiel:

```text
holzerprompt.com/process-analysis/
→ holzerprompt.com/fr/analyse-des-processus/
```

Nicht veröffentlichte oder nicht vorhandene Sprachfassungen werden für die konkrete Seite nicht als direkt verfügbare Übersetzung angeboten.

## 19. Fallback-Regel

Es gibt auf öffentlichen Sprach-URLs keinen automatischen Fallback auf Inhalte einer anderen Sprache.

Fehlt eine veröffentlichte französische Fassung, wird auf einer französischen URL nicht automatisch englischer oder deutscher Content ausgegeben.

## 20. Formulare und Systemtexte

Es wird unterschieden zwischen:

- **Django-i18n** für technische UI-Texte wie „Zurück“, „Weiter“, „Pflichtfeld“.
- **CMS-Sprachinhalten** für redaktionelle Texte wie Überschriften, Einleitungen und Bestätigungstexte.
- **CI-Machine** für KI-gestützte redaktionelle Übersetzungen.

## 21. Datenmodell – Zielkern

```text
Site
Language
SiteLanguage

Page
PageTranslation

PageBlock
PageBlockTranslation

MediaAsset
MediaAssetTranslation

Navigation
NavigationItem

KnowledgeArticle
KnowledgeArticleTranslation

Redirect
```

Später:

```text
SiteSettings
TranslationJob
TranslationRevision
```

## 22. Verbindliche Entscheidungen

- Eine gemeinsame Django-CMS-Anwendung für `.de` und `.com`.
- Deutsch ist die führende Masterquelle.
- Internationale Fassungen sind persistierte, editierbare Inhalte.
- `Page` und `PageTranslation` werden getrennt.
- Blockstruktur wird geteilt; Blocktexte werden pro Sprache gespeichert.
- Jede Site definiert ihre verfügbaren Sprachen.
- Slugs und SEO-Daten sind sprachabhängig.
- Keine öffentlichen Sprachfallbacks.
- KI-/Promptlogik gehört nicht in das CMS.
- Jede Sprache erhält eine eigene Navigation; Details stehen im Navigationsdokument.

## 23. Noch offen

- Exakte Felder und Constraints der Django-Modelle.
- Umgang mit freien internen Links innerhalb von Rich Text.
- Vollständiges Revisions-/Versionsmodell.
- Finale Strategie für `x-default`.
- Exakte Entwicklungsdomains für die zweite Site.
- Zeitpunkt für ein eigenes redaktionelles Frontend außerhalb des Django-Admins.

## 24. Umsetzungsreihenfolge

1. `Language`
2. `Site`
3. `SiteLanguage`
4. `Page` umbauen
5. `PageTranslation`
6. `PageBlock` auf Struktur/Layout reduzieren
7. `PageBlockTranslation`
8. vorhandene deutsche Testdaten migrieren
9. `MediaAssetTranslation`
10. Renderer auf Site + Sprache umstellen
11. Deutsch vollständig testen
12. Englisch manuell als zweite Sprache testen
13. Navigation site-/sprachfähig machen
14. danach CI-Machine-Automatisierung anschließen
