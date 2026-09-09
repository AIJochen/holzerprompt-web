from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Entwurf"
    PUBLISHED = "published", "Veröffentlicht"


class MediaAsset(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Bild"
        DOCUMENT = "document", "Dokument"
        OTHER = "other", "Sonstige Datei"

    title = models.CharField(
        "Titel",
        max_length=200,
        blank=True,
    )

    file = models.FileField(
        "Datei",
        upload_to="uploads/%Y/%m/",
    )

    media_type = models.CharField(
        "Medientyp",
        max_length=20,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )

    alt_text = models.CharField(
        "Alternativtext",
        max_length=300,
        blank=True,
        help_text="Für Bilder: kurze inhaltliche Beschreibung für Barrierefreiheit und SEO.",
    )

    caption = models.CharField(
        "Bildunterschrift",
        max_length=500,
        blank=True,
    )

    copyright_notice = models.CharField(
        "Copyright / Quelle",
        max_length=300,
        blank=True,
    )

    width = models.PositiveIntegerField(
        "Breite",
        null=True,
        blank=True,
    )

    height = models.PositiveIntegerField(
        "Höhe",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        "Hochgeladen",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Geändert",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Medien"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or self.file.name


class Page(models.Model):
    class TemplateType(models.TextChoices):
        STANDARD = "standard", "Standardseite"
        LANDING = "landing", "Landingpage"

    title = models.CharField(
        "Titel",
        max_length=200,
    )

    slug = models.SlugField(
        "Slug",
        max_length=200,
    )

    parent = models.ForeignKey(
        "self",
        verbose_name="Übergeordnete Seite",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )

    template_type = models.CharField(
        "Seitentyp",
        max_length=30,
        choices=TemplateType.choices,
        default=TemplateType.STANDARD,
    )

    meta_title = models.CharField(
        "Meta-Titel",
        max_length=200,
        blank=True,
    )

    meta_description = models.CharField(
        "Meta-Beschreibung",
        max_length=320,
        blank=True,
    )

    canonical_url = models.URLField(
        "Canonical URL",
        blank=True,
    )

    robots_index = models.BooleanField(
        "Indexierung erlauben",
        default=True,
    )

    robots_follow = models.BooleanField(
        "Links folgen erlauben",
        default=True,
    )

    created_at = models.DateTimeField(
        "Erstellt",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Geändert",
        auto_now=True,
    )

    published_at = models.DateTimeField(
        "Veröffentlicht am",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Seite"
        verbose_name_plural = "Seiten"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "slug"],
                name="unique_page_slug_per_parent",
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (
            self.status == PublishStatus.PUBLISHED
            and self.published_at is None
        ):
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        parts = [self.slug]

        parent = self.parent

        while parent:
            parts.insert(0, parent.slug)
            parent = parent.parent

        return "/" + "/".join(parts) + "/"


class PageBlock(models.Model):
    class BlockType(models.TextChoices):
        HERO = "hero", "Hero"
        RICH_TEXT = "rich_text", "Text"
        IMAGE_TEXT = "image_text", "Bild + Text"
        FEATURES = "features", "Features / Spalten"
        CTA = "cta", "Call-to-Action"
        FAQ = "faq", "FAQ"
        REFERENCE = "reference", "Referenz"
        FORM = "form", "Formular"
        CI_MODULE = "ci_module", "CI-Machine-Modul"

    page = models.ForeignKey(
        Page,
        verbose_name="Seite",
        on_delete=models.CASCADE,
        related_name="blocks",
    )

    block_type = models.CharField(
        "Blocktyp",
        max_length=30,
        choices=BlockType.choices,
    )

    media = models.ForeignKey(
        MediaAsset,
        verbose_name="Medium",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="page_blocks",
    )

    position = models.PositiveIntegerField(
        "Position",
        default=0,
    )

    data = models.JSONField(
        "Blockdaten",
        default=dict,
        blank=True,
        help_text="Strukturierte Inhalte des jeweiligen Blocktyps.",
    )

    is_active = models.BooleanField(
        "Aktiv",
        default=True,
    )

    created_at = models.DateTimeField(
        "Erstellt",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Geändert",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Seitenblock"
        verbose_name_plural = "Seitenblöcke"
        ordering = ["position", "id"]

    def __str__(self):
        return f"{self.page.title}: {self.get_block_type_display()}"


class Navigation(models.Model):
    name = models.CharField(
        "Name",
        max_length=100,
        unique=True,
    )

    identifier = models.SlugField(
        "Kennung",
        max_length=50,
        unique=True,
        help_text="Zum Beispiel main oder footer.",
    )

    class Meta:
        verbose_name = "Navigation"
        verbose_name_plural = "Navigationen"

    def __str__(self):
        return self.name


class NavigationItem(models.Model):
    navigation = models.ForeignKey(
        Navigation,
        verbose_name="Navigation",
        on_delete=models.CASCADE,
        related_name="items",
    )

    label = models.CharField(
        "Bezeichnung",
        max_length=100,
    )

    page = models.ForeignKey(
        Page,
        verbose_name="Interne Seite",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="navigation_items",
    )

    external_url = models.URLField(
        "Externe URL",
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        verbose_name="Übergeordneter Menüpunkt",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    position = models.PositiveIntegerField(
        "Position",
        default=0,
    )

    is_visible = models.BooleanField(
        "Sichtbar",
        default=True,
    )

    class Meta:
        verbose_name = "Navigationspunkt"
        verbose_name_plural = "Navigationspunkte"
        ordering = ["position", "id"]

    def __str__(self):
        return self.label

    @property
    def url(self):
        if self.page:
            return self.page.get_absolute_url()

        return self.external_url


class KnowledgeArticle(models.Model):
    title = models.CharField(
        "Titel",
        max_length=200,
    )

    slug = models.SlugField(
        "Slug",
        max_length=200,
        unique=True,
    )

    teaser = models.TextField(
        "Teaser",
        blank=True,
    )

    content = models.TextField(
        "Inhalt",
        blank=True,
    )

    teaser_image = models.ForeignKey(
        MediaAsset,
        verbose_name="Teaserbild",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="knowledge_articles",
    )

    category = models.CharField(
        "Kategorie",
        max_length=100,
        blank=True,
    )

    author = models.CharField(
        "Autor",
        max_length=150,
        blank=True,
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )

    meta_title = models.CharField(
        "Meta-Titel",
        max_length=200,
        blank=True,
    )

    meta_description = models.CharField(
        "Meta-Beschreibung",
        max_length=320,
        blank=True,
    )

    robots_index = models.BooleanField(
        "Indexierung erlauben",
        default=True,
    )

    robots_follow = models.BooleanField(
        "Links folgen erlauben",
        default=True,
    )

    created_at = models.DateTimeField(
        "Erstellt",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Geändert",
        auto_now=True,
    )

    published_at = models.DateTimeField(
        "Veröffentlicht am",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Wissensartikel"
        verbose_name_plural = "Wissensartikel"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (
            self.status == PublishStatus.PUBLISHED
            and self.published_at is None
        ):
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "website:knowledge_article",
            kwargs={"slug": self.slug},
        )


class Redirect(models.Model):
    source_path = models.CharField(
        "Alter Pfad",
        max_length=500,
        unique=True,
        help_text="Zum Beispiel /alte-wordpress-seite/",
    )

    target_path = models.CharField(
        "Neuer Pfad",
        max_length=500,
    )

    is_active = models.BooleanField(
        "Aktiv",
        default=True,
    )

    created_at = models.DateTimeField(
        "Erstellt",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Weiterleitung"
        verbose_name_plural = "Weiterleitungen"
        ordering = ["source_path"]

    def __str__(self):
        return f"{self.source_path} → {self.target_path}"