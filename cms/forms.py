import re

import bleach
from django import forms
from django.core.validators import URLValidator

from .models import PageBlock, PageBlockTranslation


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

RICH_TEXT_VARIANT_CHOICES = [
    ("", "Standard"),
    ("highlighted", "Hervorgehoben"),
    ("muted", "Dezent"),
]

RICH_TEXT_WIDTH_CHOICES = [
    ("", "Standard"),
    ("narrow", "Schmal"),
    ("wide", "Breit"),
]

RICH_TEXT_ALIGNMENT_CHOICES = [
    ("", "Standard"),
    ("left", "Links"),
    ("center", "Zentriert"),
]

CSS_CLASS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
HTML_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")

RICH_TEXT_ALLOWED_TAGS = [
    "p",
    "h3",
    "h4",
    "strong",
    "em",
    "a",
    "ul",
    "ol",
    "li",
    "blockquote",
    "br",
]

RICH_TEXT_ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}

RICH_TEXT_ALLOWED_PROTOCOLS = [
    "http",
    "https",
    "mailto",
]


class PageBlockStructureAdminForm(forms.ModelForm):
    # Hero – Struktur
    button_url = forms.CharField(
        required=False,
        label="Button-Ziel",
    )

    variant = forms.ChoiceField(
        required=False,
        label="Hero-Variante",
        choices=HERO_VARIANT_CHOICES,
    )

    content_alignment = forms.ChoiceField(
        required=False,
        label="Inhaltsausrichtung",
        choices=CONTENT_ALIGNMENT_CHOICES,
    )

    image_position = forms.ChoiceField(
        required=False,
        label="Bildposition",
        choices=IMAGE_POSITION_CHOICES,
    )

    image_width = forms.IntegerField(
        required=False,
        min_value=1,
        label="Bildbreite",
    )

    image_height = forms.IntegerField(
        required=False,
        min_value=1,
        label="Bildhöhe",
    )

    image_fit = forms.ChoiceField(
        required=False,
        label="Bildanpassung",
        choices=IMAGE_FIT_CHOICES,
    )

    image_loading = forms.ChoiceField(
        required=False,
        label="Bild-Ladeverhalten",
        choices=IMAGE_LOADING_CHOICES,
    )

    # Rich Text – Struktur
    rich_variant = forms.ChoiceField(
        required=False,
        label="Darstellungsvariante",
        choices=RICH_TEXT_VARIANT_CHOICES,
    )

    rich_text_width = forms.ChoiceField(
        required=False,
        label="Textbreite",
        choices=RICH_TEXT_WIDTH_CHOICES,
    )

    rich_alignment = forms.ChoiceField(
        required=False,
        label="Ausrichtung",
        choices=RICH_TEXT_ALIGNMENT_CHOICES,
    )

    # Gemeinsame technische Felder
    extra_css_classes = forms.CharField(
        required=False,
        label="Zusätzliche CSS-Klassen",
    )

    html_id = forms.CharField(
        required=False,
        label="HTML-ID",
        help_text="Ohne führendes # eingeben.",
    )

    HERO_STRUCTURAL_FIELDS = [
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
    ]

    RICH_TEXT_STRUCTURAL_FIELD_MAP = {
        "rich_variant": "variant",
        "rich_text_width": "text_width",
        "rich_alignment": "alignment",
        "extra_css_classes": "extra_css_classes",
        "html_id": "html_id",
    }

    class Meta:
        model = PageBlock
        fields = (
            "page",
            "block_type",
            "media",
            "position",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance or not self.instance.pk:
            return

        data = self.instance.data or {}

        if self.instance.block_type == PageBlock.BlockType.HERO:
            for field_name in self.HERO_STRUCTURAL_FIELDS:
                if field_name in self.fields:
                    self.fields[field_name].initial = data.get(field_name, "")

        elif self.instance.block_type == PageBlock.BlockType.RICH_TEXT:
            for form_field, data_key in self.RICH_TEXT_STRUCTURAL_FIELD_MAP.items():
                if form_field in self.fields:
                    self.fields[form_field].initial = data.get(data_key, "")

    def clean_button_url(self):
        value = (self.cleaned_data.get("button_url") or "").strip()

        if not value:
            return ""

        if value.startswith("/") or value.startswith("#"):
            return value

        validator = URLValidator(schemes=["http", "https"])
        validator(value)

        return value

    def clean_extra_css_classes(self):
        value = (self.cleaned_data.get("extra_css_classes") or "").strip()

        if not value:
            return ""

        classes = value.split()

        for css_class in classes:
            if not CSS_CLASS_RE.fullmatch(css_class):
                raise forms.ValidationError(
                    f'„{css_class}“ ist keine gültige CSS-Klasse.'
                )

        return " ".join(classes)

    def clean_html_id(self):
        value = (self.cleaned_data.get("html_id") or "").strip()

        if not value:
            return ""

        if value.startswith("#"):
            raise forms.ValidationError(
                "Bitte die HTML-ID ohne führendes # eingeben."
            )

        if not HTML_ID_RE.fullmatch(value):
            raise forms.ValidationError(
                "Die HTML-ID muss mit einem Buchstaben beginnen und darf "
                "nur Buchstaben, Zahlen, _ und - enthalten."
            )

        return value

    def clean(self):
        cleaned_data = super().clean()
        block_type = cleaned_data.get("block_type")

        if block_type == PageBlock.BlockType.HERO:
            self._complete_image_dimensions(cleaned_data)

        return cleaned_data

    def _complete_image_dimensions(self, cleaned_data):
        width = cleaned_data.get("image_width")
        height = cleaned_data.get("image_height")
        media = cleaned_data.get("media") or getattr(
            self.instance,
            "media",
            None,
        )

        if bool(width) == bool(height):
            return

        media_width = getattr(media, "width", None)
        media_height = getattr(media, "height", None)

        if not media_width or not media_height:
            message = (
                "Wenn keine Originalmaße des Bildes bekannt sind, müssen "
                "Breite und Höhe gemeinsam angegeben werden."
            )

            if width and not height:
                self.add_error("image_height", message)

            elif height and not width:
                self.add_error("image_width", message)

            return

        if width and not height:
            cleaned_data["image_height"] = round(
                width * media_height / media_width
            )

        elif height and not width:
            cleaned_data["image_width"] = round(
                height * media_width / media_height
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        block_type = self.cleaned_data.get("block_type")

        if block_type == PageBlock.BlockType.HERO:
            instance.data = {
                field_name: self.cleaned_data.get(field_name)
                for field_name in self.HERO_STRUCTURAL_FIELDS
                if self.cleaned_data.get(field_name) not in (None, "")
            }

        elif block_type == PageBlock.BlockType.RICH_TEXT:
            instance.data = {
                data_key: self.cleaned_data.get(form_field)
                for form_field, data_key in self.RICH_TEXT_STRUCTURAL_FIELD_MAP.items()
                if self.cleaned_data.get(form_field) not in (None, "")
            }

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class PageBlockTranslationAdminForm(forms.ModelForm):
    eyebrow = forms.CharField(required=False, label="Eyebrow")
    headline = forms.CharField(required=False, label="Überschrift")
    text = forms.CharField(
        required=False,
        label="Text",
        widget=forms.Textarea(attrs={"rows": 4}),
    )
    button_label = forms.CharField(
        required=False,
        label="Button-Beschriftung",
    )

    rich_heading = forms.CharField(required=False, label="Überschrift")
    rich_lead = forms.CharField(
        required=False,
        label="Einleitung / Lead",
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    rich_content = forms.CharField(
        required=False,
        label="Textinhalt",
        widget=forms.Textarea(
            attrs={
                "rows": 16,
                "class": "vLargeTextField",
                "placeholder": (
                    "<p>Text ...</p>\n"
                    "<h3>Zwischenüberschrift</h3>\n"
                    "<p>Weiterer Text ...</p>"
                ),
            }
        ),
        help_text=(
            "Erlaubt: p, h3, h4, strong, em, a, ul, ol, li, "
            "blockquote und br."
        ),
    )

    class Meta:
        model = PageBlockTranslation
        fields = (
            "page_block",
            "site_language",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance or not self.instance.pk:
            return

        data = self.instance.data or {}
        block_type = self.instance.page_block.block_type

        if block_type == PageBlock.BlockType.HERO:
            for field_name in ("eyebrow", "headline", "text", "button_label"):
                self.fields[field_name].initial = data.get(field_name, "")

        elif block_type == PageBlock.BlockType.RICH_TEXT:
            self.fields["rich_heading"].initial = data.get("heading", "")
            self.fields["rich_lead"].initial = data.get("lead", "")
            self.fields["rich_content"].initial = data.get("content", "")

    def clean_rich_content(self):
        value = (self.cleaned_data.get("rich_content") or "").strip()

        if not value:
            return ""

        return bleach.clean(
            value,
            tags=RICH_TEXT_ALLOWED_TAGS,
            attributes=RICH_TEXT_ALLOWED_ATTRIBUTES,
            protocols=RICH_TEXT_ALLOWED_PROTOCOLS,
            strip=True,
        )

    def clean(self):
        cleaned_data = super().clean()
        page_block = cleaned_data.get("page_block") or getattr(
            self.instance,
            "page_block",
            None,
        )

        if not page_block:
            return cleaned_data

        if page_block.block_type == PageBlock.BlockType.HERO:
            if not (cleaned_data.get("headline") or "").strip():
                self.add_error(
                    "headline",
                    "Die Überschrift ist erforderlich.",
                )

        elif page_block.block_type == PageBlock.BlockType.RICH_TEXT:
            if not (cleaned_data.get("rich_content") or "").strip():
                self.add_error(
                    "rich_content",
                    "Der Textinhalt ist erforderlich.",
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        page_block = self.cleaned_data.get("page_block") or instance.page_block

        if page_block.block_type == PageBlock.BlockType.HERO:
            instance.data = {
                field_name: self.cleaned_data.get(field_name)
                for field_name in ("eyebrow", "headline", "text", "button_label")
                if self.cleaned_data.get(field_name) not in (None, "")
            }

        elif page_block.block_type == PageBlock.BlockType.RICH_TEXT:
            field_map = {
                "rich_heading": "heading",
                "rich_lead": "lead",
                "rich_content": "content",
            }
            instance.data = {
                data_key: self.cleaned_data.get(form_field)
                for form_field, data_key in field_map.items()
                if self.cleaned_data.get(form_field) not in (None, "")
            }

        if commit:
            instance.save()
            self.save_m2m()

        return instance


# Existing admin.py currently imports this name.
PageBlockAdminForm = PageBlockStructureAdminForm
