from django.contrib import admin
from .forms import PageBlockAdminForm, PageBlockTranslationAdminForm

from .models import (
    KnowledgeArticle,
    Language,
    MediaAsset,
    MediaAssetTranslation,
    Navigation,
    NavigationItem,
    Page,
    PageBlock,
    PageBlockTranslation,
    PageTranslation,
    Redirect,
    Site,
    SiteLanguage,
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "native_name",
        "code",
        "is_active",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "name",
        "native_name",
        "code",
    )
    ordering = (
        "name",
    )


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "domain",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "name",
        "domain",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(SiteLanguage)
class SiteLanguageAdmin(admin.ModelAdmin):
    list_display = (
        "site",
        "language",
        "is_default",
        "url_prefix",
        "home_page",
        "position",
        "is_active",
    )
    list_filter = (
        "site",
        "language",
        "is_default",
        "is_active",
    )
    search_fields = (
        "site__name",
        "site__domain",
        "language__name",
        "language__native_name",
        "language__code",
    )
    ordering = (
        "site",
        "position",
        "language",
    )


class PageBlockInline(admin.StackedInline):
    model = PageBlock
    form = PageBlockAdminForm
    extra = 0
    ordering = ("position",)

    class Media:
        js = ("cms/js/pageblock_admin.js",)

    fieldsets = (
        (
            "Block",
            {
                "fields": (
                    "block_type",
                    "position",
                    "is_active",
                ),
            },
        ),
        (
            "Hero – Struktur",
            {
                "fields": (
                    "button_url",
                    "media",
                ),
                "classes": ("hero-fields",),
            },
        ),
        (
            "Hero – Erweitert",
            {
                "fields": (
                    "variant",
                    "content_alignment",
                    "image_position",
                    "image_width",
                    "image_height",
                    "image_fit",
                    "image_loading",
                ),
                "classes": ("collapse", "hero-fields"),
            },
        ),
        (
            "Rich Text – Erweitert",
            {
                "fields": (
                    "rich_variant",
                    "rich_text_width",
                    "rich_alignment",
                ),
                "classes": ("collapse", "rich-text-fields"),
            },
        ),
        (
            "Technisch",
            {
                "fields": (
                    "extra_css_classes",
                    "html_id",
                ),
                "classes": ("collapse",),
            },
        ),
    )


class PageTranslationInline(admin.StackedInline):
    model = PageTranslation
    extra = 0
    ordering = ("site_language", "title")
    fields = (
        "site_language", "title", "slug", "status",
        "meta_title", "meta_description", "canonical_url",
        "robots_index", "robots_follow", "published_at",
    )
    readonly_fields = ("published_at",)


@admin.register(PageTranslation)
class PageTranslationAdmin(admin.ModelAdmin):
    list_display = ("page", "site_language", "title", "slug", "status", "updated_at")
    list_filter = ("site_language", "status", "robots_index", "robots_follow")
    search_fields = (
        "page__internal_name", "title", "slug", "meta_title", "meta_description",
    )
    readonly_fields = ("created_at", "updated_at", "published_at")
    ordering = ("site_language", "title")

    fieldsets = (
        ("Sprachversion", {"fields": ("page", "site_language", "title", "slug", "status")}),
        ("SEO", {"fields": (
            "meta_title", "meta_description", "canonical_url",
            "robots_index", "robots_follow",
        )}),
        ("Zeitstempel", {
            "fields": ("created_at", "updated_at", "published_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("internal_name", "parent", "template_type", "updated_at")
    list_filter = ("template_type",)
    search_fields = ("internal_name", "translations__title", "translations__slug")
    readonly_fields = ("created_at", "updated_at")
    inlines = [PageTranslationInline, PageBlockInline]

    fieldsets = (
        ("Seite", {"fields": ("internal_name", "parent", "template_type")}),
        ("Zeitstempel", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


class MediaAssetTranslationInline(admin.StackedInline):
    model = MediaAssetTranslation
    extra = 0
    ordering = ("site_language",)
    fields = (
        "site_language",
        "title",
        "alt_text",
        "caption",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        "file",
        "media_type",
        "width",
        "height",
        "created_at",
    )

    list_filter = (
        "media_type",
        "created_at",
    )

    search_fields = (
        "file",
        "copyright_notice",
        "translations__title",
        "translations__alt_text",
        "translations__caption",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        MediaAssetTranslationInline,
    ]


@admin.register(MediaAssetTranslation)
class MediaAssetTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "media_asset",
        "site_language",
        "title",
        "updated_at",
    )
    list_filter = (
        "site_language",
    )
    search_fields = (
        "media_asset__file",
        "title",
        "alt_text",
        "caption",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "media_asset",
        "site_language",
    )


@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "status",
        "published_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "category",
        "robots_index",
        "robots_follow",
    )
    search_fields = (
        "title",
        "slug",
        "teaser",
        "content",
        "meta_title",
        "meta_description",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
    )


class NavigationItemInline(admin.TabularInline):
    model = NavigationItem
    extra = 0
    fields = (
        "label",
        "page",
        "external_url",
        "parent",
        "position",
        "is_visible",
    )
    ordering = ("position",)


@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "identifier",
    )
    search_fields = (
        "name",
        "identifier",
    )
    prepopulated_fields = {
        "identifier": ("name",),
    }
    inlines = [
        NavigationItemInline,
    ]


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = (
        "source_path",
        "target_path",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
    )
    search_fields = (
        "source_path",
        "target_path",
    )


@admin.register(PageBlockTranslation)
class PageBlockTranslationAdmin(admin.ModelAdmin):
    form = PageBlockTranslationAdminForm

    list_display = (
        "page_block",
        "site_language",
        "updated_at",
    )
    list_filter = (
        "site_language",
        "page_block__block_type",
    )
    search_fields = (
        "page_block__page__internal_name",
        "page_block__page__translations__title",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "page_block",
        "site_language",
    )

    fieldsets = (
        (
            "Zuordnung",
            {
                "fields": (
                    "page_block",
                    "site_language",
                )
            },
        ),
        (
            "Hero – Sprachinhalt",
            {
                "fields": (
                    "eyebrow",
                    "headline",
                    "text",
                    "button_label",
                ),
                "classes": ("hero-translation-fields",),
            },
        ),
        (
            "Rich Text – Sprachinhalt",
            {
                "fields": (
                    "rich_heading",
                    "rich_lead",
                    "rich_content",
                ),
                "classes": ("rich-text-translation-fields",),
            },
        ),
        (
            "Zeitstempel",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))

        if obj is None or not obj.page_block_id:
            return fieldsets

        block_type = obj.page_block.block_type

        if block_type == PageBlock.BlockType.HERO:
            hidden_class = "rich-text-translation-fields"
        elif block_type == PageBlock.BlockType.RICH_TEXT:
            hidden_class = "hero-translation-fields"
        else:
            hidden_class = None

        if hidden_class:
            fieldsets = [
                fieldset
                for fieldset in fieldsets
                if hidden_class not in fieldset[1].get("classes", ())
            ]

        return fieldsets


@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    form = PageBlockAdminForm

    class Media:
        js = ("cms/js/pageblock_admin.js",)

    list_display = (
        "page",
        "block_type",
        "position",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "block_type",
        "is_active",
    )

    search_fields = (
        "page__internal_name",
        "page__translations__title",
    )

    ordering = (
        "page",
        "position",
    )

    fieldsets = (
        (
            "Block",
            {
                "fields": (
                    "page",
                    "block_type",
                    "position",
                    "is_active",
                ),
            },
        ),
        (
            "Hero – Struktur",
            {
                "fields": (
                    "button_url",
                    "media",
                ),
                "classes": ("hero-fields",),
            },
        ),
        (
            "Hero – Erweitert",
            {
                "fields": (
                    "variant",
                    "content_alignment",
                    "image_position",
                    "image_width",
                    "image_height",
                    "image_fit",
                    "image_loading",
                ),
                "classes": ("collapse", "hero-fields"),
            },
        ),
        (
            "Rich Text – Erweitert",
            {
                "fields": (
                    "rich_variant",
                    "rich_text_width",
                    "rich_alignment",
                ),
                "classes": ("collapse", "rich-text-fields"),
            },
        ),
        (
            "Technisch",
            {
                "fields": (
                    "extra_css_classes",
                    "html_id",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "navigation",
        "page",
        "position",
        "is_visible",
    )
    list_filter = (
        "navigation",
        "is_visible",
    )
    search_fields = (
        "label",
        "page__internal_name",
        "page__translations__title",
        "external_url",
    )