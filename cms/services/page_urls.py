from django.core.exceptions import ObjectDoesNotExist

from cms.models import PageTranslation, PublishStatus


def build_page_url(page, site_language):
    """
    Erzeugt die öffentliche URL einer Seite für eine Website-Sprache.

    Beispiele:
        DE Startseite              -> /
        EN Startseite              -> /
        FR Startseite              -> /fr/
        DE Leistungen              -> /leistungen/
        DE SEO unter Leistungen    -> /leistungen/seo/
        FR SEO unter Services      -> /fr/services/seo/

    Es werden ausschließlich veröffentlichte Seitenübersetzungen
    berücksichtigt.
    """

    # Startseite der Website-Sprache
    if site_language.home_page_id == page.pk:
        return _language_root_url(site_language)

    segments = []
    current_page = page

    while current_page is not None:
        try:
            translation = PageTranslation.objects.get(
                page=current_page,
                site_language=site_language,
                status=PublishStatus.PUBLISHED,
            )
        except ObjectDoesNotExist:
            return None

        segments.append(translation.slug)
        current_page = current_page.parent

    segments.reverse()

    path = "/".join(segments)

    prefix = site_language.url_prefix.strip("/")

    if prefix:
        return f"/{prefix}/{path}/"

    return f"/{path}/"


def _language_root_url(site_language):
    """
    Erzeugt die Root-URL einer Website-Sprache.

    Standardsprache:
        /

    Sprache mit Präfix:
        /fr/
    """

    prefix = site_language.url_prefix.strip("/")

    if prefix:
        return f"/{prefix}/"

    return "/"