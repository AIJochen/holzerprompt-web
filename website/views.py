from django.http import Http404
from django.shortcuts import get_object_or_404, render

from cms.models import (
    MediaAssetTranslation,
    PageBlockTranslation,
    PageTranslation,
    PublishStatus,
)
from cms.services.site_resolver import resolve_site_context


def home(request, language_prefix=""):
    site_context = resolve_site_context(
        request,
        language_prefix=language_prefix,
    )
    site_language = site_context.site_language

    if not site_language.home_page_id:
        raise Http404(
            "Keine Startseite für diese Website-Sprache konfiguriert."
        )

    page = site_language.home_page

    page_translation = get_object_or_404(
        PageTranslation.objects.select_related(
            "page",
            "site_language",
            "site_language__site",
            "site_language__language",
        ),
        page=page,
        site_language=site_language,
        status=PublishStatus.PUBLISHED,
    )

    block_translations = {
        translation.page_block_id: translation
        for translation in PageBlockTranslation.objects.filter(
            page_block__page=page,
            page_block__is_active=True,
            site_language=site_language,
        ).select_related("page_block")
    }

    media_translations = {
        translation.media_asset_id: translation
        for translation in MediaAssetTranslation.objects.filter(
            media_asset__page_blocks__page=page,
            site_language=site_language,
        ).distinct()
    }

    blocks = []

    for block in (
        page.blocks.filter(is_active=True)
        .select_related("media")
        .order_by("position", "pk")
    ):
        translation = block_translations.get(block.pk)

        if translation is None:
            continue

        media_translation = None

        if block.media_id:
            media_translation = media_translations.get(block.media_id)

        blocks.append(
            {
                "block": block,
                "translation": translation,
                "media_translation": media_translation,
            }
        )

    context = {
        "site": site_context.site,
        "site_language": site_language,
        "page": page,
        "page_translation": page_translation,
        "blocks": blocks,
    }

    return render(
        request,
        "website/page.html",
        context,
    )