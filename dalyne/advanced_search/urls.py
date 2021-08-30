from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^filtered/data/$', apis.SubFilterListingAPI.as_view(), name='types'),
    url(r'export/shipments/$', apis.ExportAPIView.as_view(), name='shipments'),
    url(r'exporters/importers/list/$', apis.ExporterImporterList.as_view(), name='name-list'),
    url(r'ordered/data/$', apis.OrderingListingAPI.as_view(), name='ordered'),
    url(r'download/data/response/$', apis.DownloadMessage.as_view(), name='download-message'),
    url(r'search/data/response/$', apis.RequestSearchPointsAPI.as_view(), name='search-message')

]