# Rich-Text-Block – Spezifikation v0.1

## Zweck
Der Rich-Text-Block dient für normalen redaktionellen Seiteninhalt. Er ist kein freier Page-Builder. Inhalt und Semantik werden im CMS gepflegt; die Darstellung bleibt zentral im Designsystem.

## Normale Felder
- **Überschrift** – optional, Ausgabe als `h2`
- **Einleitung / Lead** – optional, hervorgehobener Einleitungstext
- **Textinhalt** – Pflichtfeld

## Erlaubte Formatierungen
Im Textinhalt sind in v0.1 nur diese Tags erlaubt:

`p`, `h3`, `h4`, `strong`, `em`, `a`, `ul`, `ol`, `li`, `blockquote`, `br`

`h1` und `h2` sind im Inhalt nicht erlaubt. Die Seiten-Hauptüberschrift gehört zum Seitenkontext/Hero; die optionale Blocküberschrift wird als `h2` ausgegeben.

## Nicht erlaubt
Keine Bilder, Tabellen, freien Layouts, Inline-CSS, `script`, `style`, `iframe`, Formulare oder freie Klassen/IDs im Rich-Text-Inhalt.

Bilder werden über eigene strukturierte Blöcke eingebunden.

## Erweitert
- Darstellungsvariante: Standard / Hervorgehoben / Dezent
- Textbreite: Standard / Schmal / Breit
- Ausrichtung: Standard / Links / Zentriert
- Zusätzliche CSS-Klassen
- HTML-ID

## JSON-Struktur
```json
{
  "heading": "Warum Prozesswissen der Ausgangspunkt ist",
  "lead": "KI-Projekte beginnen mit dem Verständnis der tatsächlichen Arbeit.",
  "content": "<p>...</p>",
  "variant": "standard",
  "text_width": "narrow",
  "alignment": "left",
  "extra_css_classes": "",
  "html_id": "prozesswissen"
}
```

## Sicherheit
Der HTML-Inhalt wird beim Speichern serverseitig mit `bleach` sanitisiert.

Erlaubte Link-Attribute:
- `href`
- `title`

Erlaubte Protokolle:
- `http`
- `https`
- `mailto`

Interne Pfade und Anker bleiben möglich.

## Editor v0.1
Zunächst wird bewusst **keine WYSIWYG-Bibliothek** eingebunden. Der Django-Admin verwendet ein größeres Textfeld. Dadurch können wir zuerst das Blocksystem testen, ohne TinyMCE/CKEditor/Tiptap festzulegen.

Das Eingabe-Widget kann später ersetzt werden, ohne Datenmodell oder Renderer zu ändern.

## Rendering
Grundstruktur:

```html
<section class="hp-richtext ...">
  <div class="container">
    <div class="hp-richtext__inner">
      <h2>...</h2>
      <p class="hp-richtext__lead">...</p>
      <div class="hp-richtext__content">...</div>
    </div>
  </div>
</section>
```

## Offene Punkte
- WYSIWYG-Editor
- interne Link-Auswahl
- eindeutige HTML-ID je Seite prüfen
- Tabellen ggf. als eigener Block
- Revisionen/Inhaltsversionen
