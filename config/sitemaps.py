from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from portfolio.views import PROJECTS


class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "about",
            "packages",
            "contact",
            "service_list",
            "project_list",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return PROJECTS

    def location(self, item):
        return reverse("project_detail", kwargs={"slug": item["slug"]})


sitemaps = {
    "pages": StaticViewSitemap,
    "projects": ProjectSitemap,
}
