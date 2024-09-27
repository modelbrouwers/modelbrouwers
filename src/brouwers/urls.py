from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic.base import RedirectView, TemplateView

from brouwers.anniversaries.views import TwentyYearsAnniversaryView
from brouwers.contact.views import ContactMessageCreateView

# FIXME: this breaks laziness
FORUM_URL = settings.PHPBB_URL
FORUM_URL = FORUM_URL[1:] if FORUM_URL.startswith("/") else FORUM_URL
FORUM_URL = FORUM_URL if FORUM_URL.endswith("/") else FORUM_URL + "/"


urlpatterns = (
    [
        # contact page because the live shop contact page email handling is horrible and gets
        # blocked by mail servers (including our own)
        path("winkel/contact", ContactMessageCreateView.as_view()),
        path("winkel/contact/", ContactMessageCreateView.as_view(), name="contact"),
        # normal application
        path("admin/rosetta/", include("rosetta.urls")),
        path("admin/", admin.site.urls),
        path("admin/", include("loginas.urls")),
        path("api/v1/", include("brouwers.api.urls", namespace="api")),
        # just a placeholder for the url
        path("", RedirectView.as_view(url="/index.php"), name="index"),
        path("20/", RedirectView.as_view(pattern_name="20-years-anniversary")),
        path(
            "20-jaar/",
            TwentyYearsAnniversaryView.as_view(),
            name="20-years-anniversary",
        ),
        path("albums/", include("brouwers.albums.urls", namespace="albums")),
        path("awards/", include("brouwers.awards.urls")),
        path(
            "brouwersdag/",
            RedirectView.as_view(permanent=True, pattern_name="brouwersdag:index"),
        ),
        path("forum_tools/", include("brouwers.forum_tools.urls")),
        path(FORUM_URL, include("brouwers.forum_tools.urls_phpbb", namespace="phpBB")),
        path(
            "group-builds/",
            include("brouwers.groupbuilds.urls", namespace="groupbuilds"),
        ),
        path(
            "kitreviews/", include("brouwers.kitreviews.urls", namespace="kitreviews")
        ),
        path("secret_santa/", TemplateView.as_view(template_name="santa_removed.html")),
        path("shirts/", TemplateView.as_view(template_name="shirts_removed.html")),
        path("builds/", include("brouwers.builds.urls", namespace="builds")),
        path("ou/", include("brouwers.online_users.urls")),
        path(
            "modelbouwdag/",
            include("brouwers.brouwersdag.urls", namespace="brouwersdag"),
        ),
        path("i18n/", include("django.conf.urls.i18n")),
        path("", include("brouwers.users.urls", namespace="users")),
        path("", include("brouwers.general.urls")),
    ]
    + staticfiles_urlpatterns()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
)


if settings.SHOP_ENABLED:
    urlpatterns.append(
        path("winkel/", include("brouwers.shop.urls", namespace="shop")),
    )


if settings.DEBUG:
    urlpatterns += [
        path("404/", TemplateView.as_view(template_name="404.html")),
        path("dev/emails/", include("brouwers.emails.urls")),
    ]

if apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
