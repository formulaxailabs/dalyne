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
