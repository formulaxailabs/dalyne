from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Dalyne APIs",
        default_version='v1',
        description="Dalyne Endpoint Description",
        contact=openapi.Contact(email="arun.bhatt077@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', include('knox.urls')),
    path('users/', include('users.urls')),
    path('import-export/', include('import_export.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', True):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False
