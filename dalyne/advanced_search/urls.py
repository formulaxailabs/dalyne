from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^filtered/data/$', apis.SubFilterListingAPI.as_view(), name='types'),
    url(r'export/shipments/$', apis.ExportAPIView.as_view(), name='shipments')
]