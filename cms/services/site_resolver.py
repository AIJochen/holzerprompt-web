from dataclasses import dataclass

from django.http import Http404

from cms.models import Site, SiteLanguage


@dataclass(frozen=True)
class SiteContext:
    site: Site
    site_language: SiteLanguage


def resolve_site_context(request, language_prefix=""):
    host = request.get_host().split(":")[0].lower()

    try:
        site = Site.objects.get(
            domain__iexact=host,
            is_active=True,
        )
    except Site.DoesNotExist as exc:
        raise Http404("Website nicht gefunden.") from exc

    site_languages = SiteLanguage.objects.select_related(
        "language",
        "home_page",
    ).filter(
        site=site,
        is_active=True,
        language__is_active=True,
    )

    if language_prefix:
        try:
            site_language = site_languages.get(
                url_prefix=language_prefix,
            )
        except SiteLanguage.DoesNotExist as exc:
            raise Http404("Sprache nicht gefunden.") from exc
    else:
        try:
            site_language = site_languages.get(
                is_default=True,
            )
        except SiteLanguage.DoesNotExist as exc:
            raise Http404(
                "Keine Standardsprache für diese Website konfiguriert."
            ) from exc

    return SiteContext(
        site=site,
        site_language=site_language,
    )