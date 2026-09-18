from dataclasses import dataclass

from django.http import Http404

from cms.models import Site, SiteLanguage


@dataclass(frozen=True)
class SiteContext:
    site: Site
    site_language: SiteLanguage


@dataclass(frozen=True)
class ResolvedPath:
    site_context: SiteContext
    page_path: str


def resolve_site(request):
    host = request.get_host().split(":")[0].lower()

    try:
        return Site.objects.get(
            domain__iexact=host,
            is_active=True,
        )
    except Site.DoesNotExist as exc:
        raise Http404("Website nicht gefunden.") from exc


def get_active_site_languages(site):
    return (
        SiteLanguage.objects
        .select_related(
            "language",
            "home_page",
        )
        .filter(
            site=site,
            is_active=True,
            language__is_active=True,
        )
    )


def resolve_site_context(request, language_prefix=""):
    site = resolve_site(request)
    site_languages = get_active_site_languages(site)

    if language_prefix:
        try:
            site_language = site_languages.get(
                url_prefix=language_prefix
            )
        except SiteLanguage.DoesNotExist as exc:
            raise Http404("Sprache nicht gefunden.") from exc
    else:
        try:
            site_language = site_languages.get(
                is_default=True
            )
        except SiteLanguage.DoesNotExist as exc:
            raise Http404(
                "Keine Standardsprache für diese Website konfiguriert."
            ) from exc

    return SiteContext(
        site=site,
        site_language=site_language,
    )


def resolve_request_path(request, path=""):
    """
    Ermittelt Site, Website-Sprache und verbleibenden Seitenpfad.

    Beispiele:

    holzerprompt.de/leistungen/seo/
        Sprache: Standard (DE)
        page_path: leistungen/seo

    holzerprompt.com/services/seo/
        Sprache: Standard (EN)
        page_path: services/seo

    holzerprompt.com/fr/services/seo/
        Sprache: FR
        page_path: services/seo
    """

    site = resolve_site(request)
    site_languages = get_active_site_languages(site)

    segments = [
        segment
        for segment in path.strip("/").split("/")
        if segment
    ]

    site_language = None

    if segments:
        first_segment = segments[0]

        try:
            site_language = site_languages.get(
                url_prefix=first_segment
            )
        except SiteLanguage.DoesNotExist:
            pass

        if site_language is not None:
            segments = segments[1:]

    if site_language is None:
        try:
            site_language = site_languages.get(
                is_default=True
            )
        except SiteLanguage.DoesNotExist as exc:
            raise Http404(
                "Keine Standardsprache für diese Website konfiguriert."
            ) from exc

    return ResolvedPath(
        site_context=SiteContext(
            site=site,
            site_language=site_language,
        ),
        page_path="/".join(segments),
    )