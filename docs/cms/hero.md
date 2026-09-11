# HolzerPrompt CMS -- Block: Hero

**Status:** Spezifikation v0.1\
**Blocktyp:** `hero`\
**Ablage im Repository:** `docs/cms/blocks/hero.md`

## 1. Zweck

Der Hero ist ein hervorgehobener Inhaltsblock, typischerweise im oberen
Bereich einer Seite. Er verbindet eine zentrale Aussage mit optionalem
Erklärungstext, Handlungsaufforderung und Bild.

Der Block soll einen klaren Standard besitzen und ohne umfangreiche
Layoutkonfiguration einsetzbar sein. Abweichungen vom Standard werden
nur über wenige definierte Optionen gesteuert.

## 2. Normalansicht

Die normale Admin-Ansicht enthält bewusst nur sechs Felder.

  -----------------------------------------------------------------------------
  Feld                  Typ                            Pflicht Verhalten
  --------------------- ---------------- --------------------- ----------------
  Eyebrow               kurzer Text                       nein Wird oberhalb
                                                               der Überschrift
                                                               ausgegeben;
                                                               entfällt bei
                                                               leerem Feld.

  Überschrift           Text                                ja Zentrale
                                                               Überschrift des
                                                               Hero.

  Text                  mehrzeiliger                      nein Kurzer
                        Text                                   erklärender
                                                               Text; entfällt
                                                               bei leerem Feld.

  Button-Beschriftung   kurzer Text                       nein Wird nur
                                                               zusammen mit
                                                               einem gültigen
                                                               Button-Ziel als
                                                               CTA ausgegeben.

  Button-Ziel           interner Pfad                     nein Ziel des CTA.
                        oder URL                               

  Bild                  `MediaAsset`                      nein Hero muss auch
                                                               ohne Bild
                                                               korrekt
                                                               funktionieren.
  -----------------------------------------------------------------------------

### 2.1 Button-Regel

Ein Button wird nur ausgegeben, wenn sowohl Beschriftung als auch Ziel
vorhanden sind. Ein einzelnes ausgefülltes Button-Feld gilt als
unvollständig und soll im Admin möglichst validiert werden.

Interne Ziele dürfen als relative Pfade gespeichert werden, z. B.
`/kontakt/`. Externe Ziele müssen als gültige URL validiert werden.

## 3. Erweiterte Einstellungen

Der Bereich „Erweitert" soll im Admin standardmäßig einklappbar sein.

  -----------------------------------------------------------------------
  Feld                    Typ                     Standard
  ----------------------- ----------------------- -----------------------
  Hero-Variante           Auswahl                 Standard

  Inhaltsausrichtung      Auswahl                 Standard des Designs

  Bildposition            Auswahl                 Standard des Designs

  Bildbreite              positive Ganzzahl in px intrinsische Breite des
                                                  `MediaAsset`

  Bildhöhe                positive Ganzzahl in px intrinsische Höhe des
                                                  `MediaAsset`

  Bildanpassung           Auswahl                 Standard des Designs

  Bild-Ladeverhalten      Auswahl                 Automatisch

  Zusätzliche CSS-Klassen Text                    keine

  HTML-ID                 Text                    keine
  -----------------------------------------------------------------------

### 3.1 Hero-Variante

V1 bietet:

-   `standard`
-   `large`
-   `compact`

Die Auswahl wird auf definierte CSS-Modifier abgebildet, z. B.
`hp-hero--large`.

### 3.2 Inhaltsausrichtung

V1 bietet:

-   `default`
-   `left`
-   `center`

`default` überlässt die Ausrichtung dem zentralen Designsystem.

### 3.3 Bildposition

V1 bietet:

-   `default`
-   `left`
-   `right`
-   `background`

`default` verwendet die im Designsystem definierte Standardposition. Die
konkrete Standardposition wird nicht redundant in jedem Datensatz
gespeichert.

### 3.4 Bildbreite und Bildhöhe

Beide Felder sind optional.

-   Feld leer → Wert aus `MediaAsset.width` bzw. `MediaAsset.height`
    verwenden.
-   Feld gesetzt → expliziten Wert als HTML-Abmessung verwenden.
-   Sind keine Maße verfügbar, muss der Renderer trotzdem gültiges HTML
    erzeugen und lässt das betreffende Attribut weg.

Die Felder steuern primär die intrinsischen HTML-Abmessungen und nicht
automatisch die sichtbare CSS-Größe.

Wenn nur eine benutzerdefinierte Dimension gesetzt wird, darf dadurch
kein unbeabsichtigtes falsches Seitenverhältnis erzeugt werden. Die
konkrete Formularvalidierung soll dies berücksichtigen; bevorzugt werden
entweder beide Werte gemeinsam überschrieben oder die fehlende Dimension
proportional aus den bekannten Originalmaßen abgeleitet.

### 3.5 Bildanpassung

V1 bietet:

-   `default`
-   `contain`
-   `cover`
-   `original`

Die Auswahl wird über definierte CSS-Klassen bzw. `object-fit`-Regeln
umgesetzt. Redakteure geben kein CSS direkt ein.

### 3.6 Bild-Ladeverhalten

V1 bietet verständliche CMS-Bezeichnungen:

-   **Automatisch**
-   **Priorisiert**
-   **Lazy Loading**

Der Renderer übersetzt diese Auswahl in geeignete HTML-Ladeattribute.
Technische Attribute wie `loading` oder `fetchpriority` werden nicht
direkt vom Redakteur eingegeben.

`Automatisch` ist der bevorzugte Standard. Die Anwendung kann dabei den
Kontext berücksichtigen; insbesondere ein zentraler Hero im sichtbaren
Startbereich soll nicht unnötig verzögert geladen werden.

### 3.7 Zusätzliche CSS-Klassen

Optional. Mehrere Klassen werden durch Leerzeichen getrennt.

Die Klassen werden zu den festen Hero-Basisklassen hinzugefügt. Sie
ersetzen diese nicht.

Beispiel:

``` text
py-5 text-center
```

kann zu folgender Ausgabe führen:

``` html
<section class="hp-hero hp-hero--standard py-5 text-center">
```

Die Eingabe muss validiert und normalisiert werden.

### 3.8 HTML-ID

Optional, z. B.:

``` text
prozessanalyse
```

Ausgabe:

``` html
<section id="prozessanalyse" class="hp-hero">
```

Die ID ist insbesondere für Sprungmarken gedacht. Eingabe erfolgt ohne
`#`. Die ID muss innerhalb einer Seite eindeutig sein.

## 4. Interne Datenstruktur

Das Bild selbst wird über `PageBlock.media` referenziert und **nicht**
im JSON gespeichert.

Ein vollständig konfigurierter Hero könnte intern beispielsweise
folgende Blockdaten enthalten:

``` json
{
    "eyebrow": "HolzerPrompt",
    "headline": "KI-Potenziale in Ihrem Unternehmen erkennen",
    "text": "Wir analysieren Ihre Geschäftsprozesse und identifizieren konkrete Ansatzpunkte für KI.",
    "button_label": "Mehr erfahren",
    "button_url": "/kontakt/",
    "variant": "large",
    "content_alignment": "left",
    "image_position": "right",
    "image_width": 1600,
    "image_height": 900,
    "image_fit": "cover",
    "image_loading": "auto",
    "extra_css_classes": "py-5",
    "html_id": "prozessanalyse"
}
```

Nicht gesetzte optionale Werte müssen nicht zwingend im JSON gespeichert
werden. Der Renderer verwendet dann die definierten Defaults.

## 5. MediaAsset-Verhalten

Das Hero-Bild wird über `PageBlock.media` ausgewählt.

Verwendet werden nach Möglichkeit:

-   `media.file.url`
-   `media.alt_text`
-   `media.width`
-   `media.height`

Der Alt-Text wird zentral am `MediaAsset` gepflegt. Der Hero soll keinen
zweiten, konkurrierenden Alt-Text im JSON erhalten.

Für rein dekorative Bilder muss später eine eindeutige Möglichkeit
vorgesehen werden, einen leeren Alt-Text (`alt=""`) bewusst zu
kennzeichnen. Bis diese Medienlogik implementiert ist, darf der Renderer
fehlenden Alt-Text nicht durch Dateinamen oder automatisch erfundene
Beschreibungen ersetzen.

## 6. Default-Verhalten

Ein minimal gültiger Hero benötigt nur eine Überschrift.

Sind optionale Felder leer:

-   Eyebrow → keine Ausgabe;
-   Text → keine Ausgabe;
-   Button → keine Ausgabe, sofern Beschriftung und Ziel nicht
    vollständig sind;
-   Bild → Hero rendert als Variante ohne Bild;
-   Variante → Standard;
-   Inhaltsausrichtung → Designstandard;
-   Bildposition → Designstandard;
-   Breite/Höhe → Maße des MediaAsset, sofern vorhanden;
-   Bildanpassung → Designstandard;
-   Ladeverhalten → automatisch;
-   zusätzliche CSS-Klassen → keine;
-   HTML-ID → kein `id`-Attribut.

Damit bleibt jeder gültige Datensatz ohne zusätzliche Konfiguration
renderbar.

## 7. HTML- und CSS-Konzept

Der Hero erhält eine feste Basisklasse:

``` html
<section class="hp-hero">
```

Varianten und Optionen werden kontrolliert in weitere Klassen übersetzt.
Die genaue DOM-Struktur bleibt Aufgabe des Templates und darf später
weiterentwickelt werden, ohne dass CMS-Inhalte angepasst werden müssen.

Bootstrap wird für Grid und responsive Grundstruktur genutzt.
Projektspezifisches Verhalten liegt in der zentralen
HolzerPrompt-CSS-Schicht.

Ein schematisches Beispiel:

``` html
<section id="prozessanalyse" class="hp-hero hp-hero--large py-5">
    <div class="container">
        <div class="row align-items-center">
            <div class="col">
                <p class="hp-hero__eyebrow">HolzerPrompt</p>
                <h1>KI-Potenziale in Ihrem Unternehmen erkennen</h1>
                <p>Wir analysieren Ihre Geschäftsprozesse.</p>
                <a class="btn btn-primary" href="/kontakt/">Mehr erfahren</a>
            </div>
            <div class="col">
                <img
                    src="/media/uploads/2026/09/hero.jpg"
                    width="1600"
                    height="900"
                    alt="..."
                >
            </div>
        </div>
    </div>
</section>
```

Dies ist ein Rendering-Beispiel, keine festgeschriebene endgültige
HTML-Struktur.

## 8. Validierung

Das Admin-Formular soll mindestens folgende Regeln prüfen:

-   Überschrift darf nicht leer sein.
-   Button-Beschriftung und Button-Ziel werden gemeinsam verwendet.
-   Button-Ziel muss ein zulässiger interner Pfad oder eine gültige
    externe URL sein.
-   Bildbreite und Bildhöhe müssen positive Ganzzahlen sein.
-   Auswahlfelder akzeptieren nur definierte Werte.
-   zusätzliche CSS-Klassen enthalten nur zulässige Klassennamen.
-   HTML-ID enthält einen gültigen ID-Wert und soll auf der Seite
    eindeutig sein.
-   Bildbezogene Einstellungen dürfen auch ohne Bild gespeichert werden,
    sollen im Formular aber möglichst verständlich behandelt werden.

## 9. Barrierefreiheit und Semantik

-   Der Hero wird als semantischer Seitenbereich gerendert.
-   Die Überschriftenhierarchie der Gesamtseite muss berücksichtigt
    werden. Für den typischen Seiten-Hero ist eine `h1` naheliegend;
    langfristig sollte der Renderer jedoch verhindern, dass durch
    mehrere Hero-Blöcke unkontrolliert mehrere Hauptüberschriften
    entstehen.
-   Bilder benötigen einen sinnvollen Alt-Text, sofern sie inhaltliche
    Bedeutung haben.
-   Dekorative Bilder erhalten `alt=""`.
-   Buttons werden als Links gerendert, wenn sie zu einer URL
    navigieren.
-   Kontrast, Fokusdarstellung und responsive Bedienbarkeit werden
    zentral im Designsystem sichergestellt.

## 10. SEO und Performance

-   Die Hero-Überschrift soll als wesentlicher Seiteninhalt serverseitig
    im HTML vorhanden sein.
-   Zentrale Hero-Bilder dürfen im Automatikmodus nicht unnötig lazy
    geladen werden.
-   Intrinsische Bildmaße werden nach Möglichkeit ausgegeben, damit der
    Browser den Platz vor dem Laden reservieren kann.
-   Responsive Bildvarianten (`srcset`/`sizes`) sind perspektivisch
    vorgesehen, sobald ein Rendition-System existiert.
-   Alt-Texte werden nicht automatisch aus Dateinamen erzeugt.

## 11. Bewusst nicht Bestandteil von v0.1

Folgende Optionen werden zunächst **nicht** in das Hero-Formular
aufgenommen:

-   zweiter CTA;
-   frei wählbare Button-Stile;
-   freie Farben und Hintergrundfarben;
-   freie Schriftgrößen;
-   individuelle Innen-/Außenabstände als Zahlenwerte;
-   freie maximale Inhaltsbreite;
-   Breakpoint-Konfiguration;
-   separates Mobile-Bild;
-   Fokuspunkt/Cropping;
-   Overlay-Farbe und Overlay-Deckkraft;
-   Animationen;
-   frei eingegebenes CSS oder JavaScript;
-   frei editierbares HTML.

Diese Funktionen können später ergänzt werden, wenn ein konkreter Bedarf
entsteht.

## 12. Spätere Erweiterungen

Mögliche spätere Erweiterungen:

-   automatisches Auslesen von Bildbreite und -höhe beim Upload;
-   responsive Renditions und `srcset`;
-   WebP-/AVIF-Erzeugung;
-   separates Mobile-Bild, falls sich ein realer Bedarf zeigt;
-   Fokuspunkt und kontrolliertes Cropping;
-   interne Seitenauswahl statt manueller Eingabe eines internen
    Button-Pfads;
-   Vorschau des Hero direkt im Admin;
-   blocktypspezifische Live-Validierung.

Diese Punkte sind ausdrücklich keine Voraussetzung für Hero v1.
