from django.shortcuts import get_object_or_404, render

from cms.models import Page, PublishStatus


def home(request):
    page = get_object_or_404(
        Page,
        slug="startseite",
        parent__isnull=True,
        status=PublishStatus.PUBLISHED,
    )

    return render(
        request,
        "website/page.html",
        {
            "page": page,
        },
    )