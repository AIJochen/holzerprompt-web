from django.contrib import admin
from .forms import PageBlockAdminForm

from .models import (
    KnowledgeArticle,
    Language,
    MediaAsset,
    Navigation,
    NavigationItem,
    Page,
    PageBlock,
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
            "Hero – Inhalt",
            {
                "fields": (
                    "eyebrow",
                    "headline",
                    "text",
                    "button_label",
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
            "Rich Text – Inhalt",
            {
                "fields": (
                    "rich_heading",
                    "rich_lead",
                    "rich_content",
                ),
                "classes": ("rich-text-fields",),
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "parent",
        "template_type",
        "status",
        "updated_at",
    )
    list_filter = (
        "status",
        "template_type",
        "robots_index",
        "robots_follow",
    )
    search_fields = (
        "title",
        "slug",
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
    inlines = [
        PageBlockInline,
    ]

    fieldsets = (
        (
            "Seite",
            {
                "fields": (
                    "title",
                    "slug",
                    "parent",
                    "status",
                    "template_type",
                )
            },
        ),
        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "canonical_url",
                    "robots_index",
                    "robots_follow",
                )
            },
        ),
        (
            "Zeitstempel",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "published_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "media_type",
        "file",
        "width",
        "height",
        "created_at",
    )
    list_filter = (
        "media_type",
        "created_at",
    )
    search_fields = (
        "title",
        "alt_text",
        "caption",
        "copyright_notice",
        "file",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
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
        "page__title",
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
            "Hero – Inhalt",
            {
                "fields": (
                    "eyebrow",
                    "headline",
                    "text",
                    "button_label",
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
            "Rich Text – Inhalt",
            {
                "fields": (
                    "rich_heading",
                    "rich_lead",
                    "rich_content",
                ),
                "classes": ("rich-text-fields",),
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
        "page__title",
        "external_url",
    )