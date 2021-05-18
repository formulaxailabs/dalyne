from rest_framework import serializers
from core_module.models import ImportTable, ExportTable, Plans,\
    ProductMaster, CompanyMaster


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

class ProductMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaster
        fields = ('id','hs_code','description')


class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMaster
        fields = ('id','iec_code','name')


class ProductImportSerializer(serializers.Serializer):

    products_file = serializers.FileField(
        required=True
    )

    class Meta:
        fields = (
            'product_file'
        )


class CompanyImportSerializer(serializers.Serializer):

    company_file = serializers.FileField(
        required=True
    )

    class Meta:
        fields = (
            'company_file'
        )

