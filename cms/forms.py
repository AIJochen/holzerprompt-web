import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .models import PageBlock


HERO_VARIANT_CHOICES = [
    ("", "Standard"),
    ("large", "Groß"),
    ("compact", "Kompakt"),
]

CONTENT_ALIGNMENT_CHOICES = [
    ("", "Standard"),
    ("left", "Links"),
    ("center", "Zentriert"),
]

IMAGE_POSITION_CHOICES = [
    ("", "Standard"),
    ("left", "Links"),
    ("right", "Rechts"),
    ("background", "Hintergrund"),
]

IMAGE_FIT_CHOICES = [
    ("", "Standard"),
    ("contain", "Einpassen"),
    ("cover", "Ausfüllen"),
    ("original", "Originalgröße"),
]

IMAGE_LOADING_CHOICES = [
    ("", "Automatisch"),
    ("priority", "Priorisiert"),
    ("lazy", "Lazy Loading"),
]


CSS_CLASS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
HTML_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


class PageBlockAdminForm(forms.ModelForm):
    # ---------------------------------------------------------
    # Normale Hero-Felder
    # ---------------------------------------------------------

    eyebrow = forms.CharField(
        label="Eyebrow",
        required=False,
        max_length=150,
        help_text="Optionaler kurzer Text oberhalb der Überschrift.",
    )

    headline = forms.CharField(
        label="Überschrift",
        required=False,
        max_length=250,
    )

    text = forms.CharField(
        label="Text",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    button_label = forms.CharField(
        label="Button-Beschriftung",
        required=False,
        max_length=100,
    )

    button_url = forms.CharField(
        label="Button-Ziel",
        required=False,
        max_length=500,
        help_text=(
            "Interner Pfad, z. B. /kontakt/, Sprungmarke wie #kontakt "
            "oder vollständige externe URL."
        ),
    )

    # ---------------------------------------------------------
    # Erweiterte Hero-Felder
    # ---------------------------------------------------------

    variant = forms.ChoiceField(
        label="Hero-Variante",
        required=False,
        choices=HERO_VARIANT_CHOICES,
    )

    content_alignment = forms.ChoiceField(
        label="Inhaltsausrichtung",
        required=False,
        choices=CONTENT_ALIGNMENT_CHOICES,
    )

    image_position = forms.ChoiceField(
        label="Bildposition",
        required=False,
        choices=IMAGE_POSITION_CHOICES,
    )

    image_width = forms.IntegerField(
        label="Bildbreite",
        required=False,
        min_value=1,
        help_text="Optional in Pixeln. Leer = Breite des MediaAsset verwenden.",
    )

    image_height = forms.IntegerField(
        label="Bildhöhe",
        required=False,
        min_value=1,
        help_text="Optional in Pixeln. Leer = Höhe des MediaAsset verwenden.",
    )

    image_fit = forms.ChoiceField(
        label="Bildanpassung",
        required=False,
        choices=IMAGE_FIT_CHOICES,
    )

    image_loading = forms.ChoiceField(
        label="Bild-Ladeverhalten",
        required=False,
        choices=IMAGE_LOADING_CHOICES,
    )

    extra_css_classes = forms.CharField(
        label="Zusätzliche CSS-Klassen",
        required=False,
        max_length=500,
        help_text=(
            "Optional. Mehrere Klassen durch Leerzeichen trennen. "
            "Nur für gezielte Layout- oder Bootstrap-Ergänzungen."
        ),
    )

    html_id = forms.CharField(
        label="HTML-ID",
        required=False,
        max_length=150,
        help_text=(
            "Optional. Für Sprungmarken oder technische Referenzen. "
            "Ohne # eingeben."
        ),
    )

    class Meta:
        model = PageBlock
        fields = (
            "block_type",
            "media",
            "position",
            "is_active",
        )

    HERO_DATA_FIELDS = (
        "eyebrow",
        "headline",
        "text",
        "button_label",
        "button_url",
        "variant",
        "content_alignment",
        "image_position",
        "image_width",
        "image_height",
        "image_fit",
        "image_loading",
        "extra_css_classes",
        "html_id",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance or not self.instance.pk:
            return

        if self.instance.block_type != PageBlock.BlockType.HERO:
            return

        data = self.instance.data or {}

        for field_name in self.HERO_DATA_FIELDS:
            if field_name in data:
                self.fields[field_name].initial = data[field_name]

    def clean_button_url(self):
        value = self.cleaned_data.get("button_url", "").strip()

        if not value:
            return ""

        # Interner Pfad oder Sprungmarke
        if value.startswith("/") or value.startswith("#"):
            return value

        # Externe URL
        validator = URLValidator(
            schemes=["http", "https"]
        )

        try:
            validator(value)
        except ValidationError:
            raise ValidationError(
                "Bitte einen internen Pfad wie /kontakt/, "
                "eine Sprungmarke wie #kontakt oder eine vollständige "
                "http-/https-URL eingeben."
            )

        return value

    def clean_extra_css_classes(self):
        value = self.cleaned_data.get(
            "extra_css_classes",
            "",
        ).strip()

        if not value:
            return ""

        classes = value.split()

        invalid_classes = [
            css_class
            for css_class in classes
            if not CSS_CLASS_RE.match(css_class)
        ]

        if invalid_classes:
            raise ValidationError(
                "Ungültige CSS-Klasse(n): "
                + ", ".join(invalid_classes)
            )

        # Whitespace normalisieren
        return " ".join(classes)

    def clean_html_id(self):
        value = self.cleaned_data.get("html_id", "").strip()

        if not value:
            return ""

        if value.startswith("#"):
            raise ValidationError(
                "Die HTML-ID bitte ohne # eingeben."
            )

        if not HTML_ID_RE.match(value):
            raise ValidationError(
                "Die HTML-ID muss mit einem Buchstaben beginnen "
                "und darf nur Buchstaben, Zahlen, _ und - enthalten."
            )

        return value

    def clean(self):
        cleaned_data = super().clean()

        block_type = cleaned_data.get("block_type")

        # Die folgenden Regeln gelten nur für Hero-Blöcke.
        if block_type != PageBlock.BlockType.HERO:
            return cleaned_data

        headline = cleaned_data.get("headline", "").strip()

        if not headline:
            self.add_error(
                "headline",
                "Für einen Hero ist eine Überschrift erforderlich.",
            )

        button_label = cleaned_data.get(
            "button_label",
            "",
        ).strip()

        button_url = cleaned_data.get(
            "button_url",
            "",
        ).strip()

        if button_label and not button_url:
            self.add_error(
                "button_url",
                "Zu einer Button-Beschriftung muss ein Button-Ziel angegeben werden.",
            )

        if button_url and not button_label:
            self.add_error(
                "button_label",
                "Zu einem Button-Ziel muss eine Button-Beschriftung angegeben werden.",
            )

        self._complete_image_dimensions(cleaned_data)

        return cleaned_data

    def _complete_image_dimensions(self, cleaned_data):
        """
        Wenn nur Breite oder Höhe überschrieben wurde, versuchen wir,
        die fehlende Dimension proportional aus dem MediaAsset abzuleiten.
        """

        width = cleaned_data.get("image_width")
        height = cleaned_data.get("image_height")
        media = cleaned_data.get("media")

        # Beide gesetzt oder beide leer: nichts zu tun.
        if (width and height) or (not width and not height):
            return

        if not media or not media.width or not media.height:
            if width and not height:
                self.add_error(
                    "image_height",
                    "Bitte auch die Bildhöhe angeben, da für das "
                    "MediaAsset keine Originalmaße gespeichert sind.",
                )

            if height and not width:
                self.add_error(
                    "image_width",
                    "Bitte auch die Bildbreite angeben, da für das "
                    "MediaAsset keine Originalmaße gespeichert sind.",
                )

            return

        if width and not height:
            calculated_height = round(
                width * media.height / media.width
            )
            cleaned_data["image_height"] = calculated_height

        elif height and not width:
            calculated_width = round(
                height * media.width / media.height
            )
            cleaned_data["image_width"] = calculated_width

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Daten anderer Blocktypen nicht versehentlich überschreiben.
        if instance.block_type == PageBlock.BlockType.HERO:
            data = {}

            for field_name in self.HERO_DATA_FIELDS:
                value = self.cleaned_data.get(field_name)

                # Leere Default-Werte brauchen wir nicht im JSON.
                if value not in ("", None):
                    data[field_name] = value

            instance.data = data

        if commit:
            instance.save()
            self.save_m2m()

        return instance