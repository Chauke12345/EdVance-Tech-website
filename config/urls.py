from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('portal/', include('client_portal.urls')),
    path('portal/contracts/', include('contracts.urls')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('projects/', include('portfolio.urls')),
    path('services/', include('services.urls')),
]

