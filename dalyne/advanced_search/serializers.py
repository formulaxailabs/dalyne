from rest_framework import serializers
from core_module.models import ImportTable, ExportTable


class ImporterNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExportTable
        fields = ('IMPORTER_NAME',)


class ExporterNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImportTable
        fields = ('EXPORTER_NAME',)


class ExportSerializer(serializers.Serializer):
    search_id = serializers.CharField(
        required=False,
        allow_null=True
    )
    exporter = serializers.CharField(
        required=False,
        allow_null=True
    )
    importer = serializers.CharField(
        required=False,
        allow_null=True
    )
    uqc = serializers.CharField(
        required=False,
        allow_null=True
    )
    country = serializers.CharField(
        required=False,
        allow_null=True
    )
    port_of_discharge = serializers.CharField(
        required=False,
        allow_null=True
    )
    port_of_loading = serializers.CharField(
        required=False,
        allow_null=True
    )
    mode = serializers.CharField(
        required=False,
        allow_null=True
    )
    port_code = serializers.CharField(
        required=False,
        allow_null=True
    )
    hs_code = serializers.CharField(
        required=False,
        allow_null=True
    )
    description = serializers.CharField(
        required=False,
        allow_null=True
    )
    min_qty = serializers.CharField(
        required=False,
        allow_null=True
    )
    max_qty = serializers.CharField(
        required=False,
        allow_null=True
    )
    select_all = serializers.BooleanField(
        default=False
    )
    ids = serializers.JSONField(
        default=list,
        required=False,
        allow_null=True
    )

    class Meta:
        fields = (
            'search_id', 'select_all', 'ids', 'exporter', 'importer', 'uqc', 'country',
            'port_of_discharge', 'port_of_loading', 'mode', 'port_code', 'hs_code',
            'description', 'min_qty', 'max_qty'
        )

