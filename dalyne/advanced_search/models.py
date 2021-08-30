from django.db import models
from core_module.models import User, Tenant
from django.utils.translation import gettext_lazy as _

# Create your models here.


class RequestedDownloadModel(models.Model):
    Search = "search"
    Download = "download"

    REQUEST_TYPE = (
        (Search, _("search")),
        (Download, _("download"))
    )
    tenant = models.ForeignKey(
        Tenant,
        null=True,
        blank=True,
        related_name="user_downloads",
        on_delete=models.CASCADE
    )
    downloaded_ids = models.JSONField(
        default=list,
        null=True,
        blank=True
    )
    remaining_points = models.IntegerField(
        null=True,
        blank=True
    )
    request_type = models.CharField(
        choices=REQUEST_TYPE,
        null=True,
        blank=True,
        max_length=20
    )
    remaining_search_points = models.IntegerField(
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    modified_on = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )