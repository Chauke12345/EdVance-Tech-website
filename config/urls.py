from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from .sitemaps import sitemaps
from .robots import robots_txt

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("portal/", include("client_portal.urls")),
    path("portal/contracts/", include("contracts.urls")),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("projects/", include("portfolio.urls")),
    path("services/", include("services.urls")),
]
