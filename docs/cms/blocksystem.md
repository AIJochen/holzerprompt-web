# HolzerPrompt CMS -- Blocksystem

**Status:** Spezifikation v0.1\
**Geltungsbereich:** `holzerprompt-web`\
**Ablage im Repository:** `docs/cms/blocksystem.md`

## 1. Ziel

Das Blocksystem bildet die redaktionelle Grundlage der
HolzerPrompt-Website. Seiten bestehen aus geordneten
`PageBlock`-Elementen. Jeder Blocktyp besitzt eine klar definierte
Aufgabe, ein Standarddesign und eine begrenzte Zahl sinnvoller Optionen.

Das CMS soll ausdrücklich **kein universeller Page Builder** werden.
Redakteure sollen Inhalte und notwendige Varianten steuern können, ohne
das zentrale Designsystem auf Ebene einzelner Seiten nachbauen zu
müssen.

## 2. Grundprinzipien

1.  **Inhalt vor Gestaltung:** Inhaltliche Felder stehen im Vordergrund.
    Gestaltungsoptionen werden nur angeboten, wenn sie einen
    wiederkehrenden praktischen Nutzen haben.
2.  **Sinnvolle Defaults:** Jeder Block muss auch dann korrekt rendern,
    wenn optionale Darstellungsfelder leer bleiben.
3.  **Optionen überschreiben Standards:** Leere optionale Felder
    bedeuten nicht „unbestimmt", sondern „Standard des Designsystems
    verwenden".
4.  **Zentrale Gestaltung:** Die konkrete visuelle Gestaltung wird
    möglichst zentral über Bootstrap und eine kleine
    HolzerPrompt-CSS-Schicht geregelt.
5.  **Keine freie Stilprogrammierung im CMS:** Farben, Abstände,
    Schriftgrößen, Breakpoints und ähnliche Details werden nicht für
    jeden Block frei konfigurierbar gemacht.
6.  **Kontrollierte Erweiterbarkeit:** Zusätzliche CSS-Klassen und eine
    optionale HTML-ID erlauben begründete Sonderfälle, ohne das
    Datenmodell für jede Ausnahme zu erweitern.
7.  **Strukturierte Medien:** Bilder und Dateien werden über
    `MediaAsset` referenziert. Absolute Medien-URLs werden nicht in
    Blockdaten gespeichert.
8.  **Technisch sauberes HTML:** Templates/Renderer erzeugen
    semantisches, responsives und performantes HTML. Redakteure müssen
    keine technischen HTML-Attribute kennen.
9.  **Progressive Erweiterung:** Neue Felder werden erst ergänzt, wenn
    ein konkreter Bedarf entsteht. Version 1 bleibt bewusst schlank.

## 3. Datenmodell und Blockdaten

`PageBlock` enthält weiterhin:

-   `block_type`
-   `media` als optionale Beziehung zu `MediaAsset`
-   `position`
-   `data` als `JSONField`
-   `is_active`

Das `JSONField` bleibt die flexible technische Speicherung. Im Django
Admin soll es für unterstützte Blocktypen jedoch **nicht als rohes
JSON-Eingabefeld** bedient werden. Stattdessen erhält jeder Blocktyp
eine verständliche Eingabemaske. Die Formularwerte werden intern in
`data` gespeichert.

Medien werden nicht als Pfad oder URL im JSON gespeichert, wenn dafür
eine Modellbeziehung vorgesehen ist.

## 4. Normalansicht und „Erweitert"

Jeder komplexere Block kann zwei Bedienebenen besitzen:

### Normalansicht

Enthält nur Felder, die beim normalen redaktionellen Arbeiten regelmäßig
benötigt werden.

### Erweitert

Enthält optionale Layout-, Rendering- und technische Einstellungen. Der
Bereich soll im Admin standardmäßig einklappbar sein.

Ein leer gelassenes Feld unter „Erweitert" verwendet grundsätzlich den
definierten Standardwert des Renderers bzw. Designsystems.

## 5. CSS- und Designsystem

Für Version 1 wird eine möglichst kleine CSS-Landschaft angestrebt:

-   Bootstrap als Basis für Grid, responsive Hilfsklassen und
    grundlegende UI-Strukturen.
-   Eine zusätzliche zentrale HolzerPrompt-CSS-Datei bzw. eine kleine,
    zentral verwaltete CSS-Schicht für projektspezifische Komponenten.
-   Blockkomponenten erhalten stabile eigene Basisklassen, z. B.
    `hp-hero`.
-   Varianten erhalten kontrollierte Modifier-Klassen, z. B.
    `hp-hero--large`.
-   Im CMS eingetragene zusätzliche Klassen werden nur **ergänzt**; sie
    ersetzen niemals die Basisklasse eines Blocks.

Beispiel:

``` html
<section class="hp-hero hp-hero--standard py-5">
```

Nicht vorgesehen ist, die komplette Gestaltung eines Blocks
ausschließlich über frei eingegebene Bootstrap-Klassen im CMS
zusammenzustellen.

## 6. Zusätzliche CSS-Klassen

Blocktypen können unter „Erweitert" das Feld **Zusätzliche CSS-Klassen**
erhalten.

Regeln:

-   optional;
-   mehrere Klassen werden durch Leerzeichen getrennt;
-   geeignet für gezielte Bootstrap-Hilfsklassen oder definierte
    projektspezifische Klassen;
-   keine vollständige Ersetzung des Blockdesigns;
-   Eingabe wird serverseitig validiert/normalisiert;
-   Klassen dürfen keine HTML-Fragmente oder sonstigen Markup-Code
    enthalten.

Hilfetext im Admin:

> Optional. Mehrere Klassen durch Leerzeichen trennen. Nur für gezielte
> Layout- oder Bootstrap-Ergänzungen.

## 7. HTML-ID

Blocktypen können eine optionale **HTML-ID** erhalten.

Zweck:

-   Sprungmarken, z. B. `/leistungen/#prozessanalyse`;
-   gezielte technische Referenzen;
-   gegebenenfalls klar begrenzte JavaScript-Anbindungen.

Regeln:

-   Eingabe ohne `#`;
-   IDs sollen nicht als primäres Styling-Instrument verwendet werden;
-   pro gerenderter Seite muss eine ID eindeutig sein;
-   Eingabe wird auf gültige ID-Werte validiert.

Hilfetext im Admin:

> Optional. Für Sprungmarken oder technische Referenzen. Ohne `#`
> eingeben.

## 8. Medien und Bildabmessungen

`MediaAsset` ist die zentrale Medienreferenz. Für Bilder sollen
tatsächliche Pixelbreite und Pixelhöhe langfristig beim Upload
automatisch ermittelt und in `MediaAsset.width` und `MediaAsset.height`
gespeichert werden.

Wenn ein Block keine eigenen Werte für Bildbreite oder Bildhöhe vorgibt,
verwendet der Renderer die intrinsischen Maße des `MediaAsset` für die
HTML-Attribute `width` und `height`, sofern diese bekannt sind.

Beispiel:

``` html
<img
    src="/media/uploads/2026/09/hero.jpg"
    width="1600"
    height="900"
    alt="..."
>
```

Die sichtbare responsive Größe wird weiterhin über CSS geregelt. Die
HTML-Abmessungen dienen insbesondere dazu, dem Browser das
Seitenverhältnis frühzeitig bekannt zu machen und Layout-Verschiebungen
zu reduzieren.

Ein späteres Rendition-System für WebP/AVIF, responsive Bildgrößen,
Cropping und Fokuspunkt bleibt möglich, ist aber nicht Bestandteil von
v0.1.

## 9. Rendering und Sicherheit

-   CMS-Inhalte werden über Django Templates ausgegeben und
    standardmäßig escaped.
-   Freie CSS-Klassen und HTML-IDs werden validiert, bevor sie in
    Attribute übernommen werden.
-   Blocktypen rendern nur bekannte, definierte Datenfelder.
-   Fehlende optionale Daten dürfen keinen Templatefehler verursachen.
-   Ein unbekannter oder noch nicht implementierter Blocktyp soll im
    Produktionsbetrieb die Seite nicht zerstören.
-   Nicht aktive Blöcke (`is_active=False`) werden nicht ausgegeben.
-   Die Reihenfolge wird über `position` bestimmt.

## 10. Erweiterungsprinzip

Für jeden neuen Blocktyp wird unter `docs/cms/blocks/` eine eigene
Spezifikation angelegt. Erst danach werden Admin-Formular, Validierung
und Renderer implementiert.

Die Spezifikation eines Blocks dokumentiert mindestens:

-   Zweck;
-   Normalansicht;
-   erweiterte Einstellungen;
-   Defaults;
-   interne Datenstruktur;
-   Validierung;
-   MediaAsset-Verhalten;
-   HTML-/CSS-Rendering;
-   Barrierefreiheit und SEO, soweit relevant;
-   bewusst nicht enthaltene Funktionen;
-   mögliche spätere Erweiterungen.
