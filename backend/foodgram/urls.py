from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('s/', include('recipes.short_links')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
