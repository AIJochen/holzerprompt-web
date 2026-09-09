from django.contrib import admin

from .models import (
    KnowledgeArticle,
    MediaAsset,
    Navigation,
    NavigationItem,
    Page,
    PageBlock,
    Redirect,
)


class PageBlockInline(admin.StackedInline):
    model = PageBlock
    extra = 0
    fields = (
        "block_type",
        "media",
        "position",
        "is_active",
        "data",
    )
    ordering = ("position",)


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