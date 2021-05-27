from rest_framework import serializers, fields
from core_module.models import ImportTable, ExportTable, Plans,\
    ProductMaster, CompanyMaster, CountryMaster, FilterDataModel


class ImporterDataFilterSerializer(serializers.ModelSerializer):
    iec = serializers.SerializerMethodField()

    def get_iec(self, obj):
        return obj.IMPORTER_ID

    class Meta:
        model = ImportTable
        fields = ('RITC', 'RITC_DISCRIPTION', 'UQC', 'QUANTITY', 'IMPORTER_NAME',
                  'EXPORTER_NAME', 'CURRENCY', 'COUNTRY_OF_ORIGIN', 'PORT_OF_LOADING', 'PORT_OF_DISCHARGE',
                  'MODE_OF_PORT', 'PORT_CODE', 'iec', 'MONTH', 'YEAR')


class ExporterDataFilterSerializer(serializers.ModelSerializer):
    iec = serializers.SerializerMethodField()

    def get_iec(self, obj):
        return obj.EXPORTER_ID

    class Meta:
        model = ExportTable
        fields = ('RITC', 'RITC_DISCRIPTION', 'UQC', 'QUANTITY', 'IMPORTER_NAME',
                  'EXPORTER_NAME', 'CURRENCY', 'COUNTRY_OF_ORIGIN', 'PORT_OF_LOADING', 'PORT_OF_DISCHARGE',
                  'MODE_OF_PORT', 'PORT_CODE', 'iec', 'MONTH', 'YEAR')
