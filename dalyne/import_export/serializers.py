from rest_framework import serializers
from core_module.models import ImportTable


class ExcelDataImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportTable
        fields = '__all__'
