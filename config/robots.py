from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent: *
Allow: /

Disallow: /admin/
Disallow: /portal/
Disallow: /staff/

Sitemap: https://edvance-tech-website-production.up.railway.app/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
