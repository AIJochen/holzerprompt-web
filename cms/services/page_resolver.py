from django.http import Http404

from cms.models import PageTranslation, PublishStatus


def resolve_page(site_language, page_path):
    """
    Löst einen hierarchischen URL-Pfad innerhalb einer Website-Sprache auf.

    Beispiel:
        leistungen/seo

    wird schrittweise aufgelöst als:
        parent=None  + slug=leistungen
        parent=Page  + slug=seo
    """

    segments = [
        segment
        for segment in page_path.strip("/").split("/")
        if segment
    ]

    if not segments:
        raise Http404("Kein Seitenpfad angegeben.")

    parent_page = None
    page_translation = None

    for segment in segments:
        try:
            page_translation = (
                PageTranslation.objects
                .select_related("page", "site_language")
                .get(
                    site_language=site_language,
                    slug=segment,
                    page__parent=parent_page,
                    status=PublishStatus.PUBLISHED,
                )
            )
        except PageTranslation.DoesNotExist as exc:
            raise Http404("Seite nicht gefunden.") from exc
        except PageTranslation.MultipleObjectsReturned as exc:
            raise Http404(
                "Seitenpfad ist nicht eindeutig konfiguriert."
            ) from exc

        parent_page = page_translation.page

    return page_translation