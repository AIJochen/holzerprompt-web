from django.shortcuts import get_object_or_404, render

from cms.models import PageBlockTranslation, PageTranslation, PublishStatus


def home(request):
    page_translation = get_object_or_404(
        PageTranslation.objects.select_related(
            "page",
            "site_language",
            "site_language__site",
            "site_language__language",
        ),
        page__parent__isnull=True,
        site_language__site__domain="holzerprompt.de",
        site_language__language__code="de",
        site_language__is_active=True,
        site_language__site__is_active=True,
        site_language__language__is_active=True,
        status=PublishStatus.PUBLISHED,
        slug="startseite",
    )

    page = page_translation.page
    site_language = page_translation.site_language

    block_translations = {
        translation.page_block_id: translation
        for translation in PageBlockTranslation.objects.filter(
            page_block__page=page,
            page_block__is_active=True,
            site_language=site_language,
        ).select_related("page_block")
    }

    blocks = []

    for block in page.blocks.filter(is_active=True).order_by("position", "pk"):
        translation = block_translations.get(block.pk)

        if translation is None:
            continue

        blocks.append(
            {
                "block": block,
                "translation": translation,
            }
        )

    return render(
        request,
        "website/page.html",
        {
            "page": page,
            "page_translation": page_translation,
            "site_language": site_language,
            "blocks": blocks,
        },
    )