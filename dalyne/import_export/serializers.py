from rest_framework import serializers
from core_module.models import ImportTable, ExportTable, Plans


class PlansListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = '__all__'


class ExcelDataImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTable
        fields = '__all__'

class ImportViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTable
        fields = '__all__'

class ExportViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportTable
        fields = '__all__'
