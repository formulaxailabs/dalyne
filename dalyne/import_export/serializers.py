from rest_framework import serializers, fields
from core_module.models import ImportTable, ExportTable, Plans,\
    ProductMaster, CompanyMaster, CountryMaster

file_choice_field = [
    ("import", "Import"),
    ("export", "Export")
]

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


class ExportImportUploadSerializer(serializers.Serializer):

    file = serializers.FileField(
        required=True
    )
    type_of_sheet = fields.ChoiceField(
        choices=file_choice_field,
        required=True
    )
    country_id = serializers.IntegerField(
        required=True,
        allow_null=False
    )

    def validate_country_id(self, country_id):
        if not CountryMaster.objects.filter(id=country_id):
            raise serializers.ValidationError("Invalid Country id")
        return country_id


    class Meta:
        fields = (
            'file', 'type_of_sheet', ' country_id'
        )


class CountryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryMaster
        fields = ('id', 'name')


