from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^create/order/$', apis.TransactionAPI.as_view(), name='transactions'),
    url(r'^capture/payment/$', apis.CapturePaymentAPI.as_view(), name='payment'),

]