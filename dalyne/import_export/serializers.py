from rest_framework import serializers, fields
from core_module.models import ImportTable, ExportTable, Plans,\
    ProductMaster, CompanyMaster, CountryMaster, FilterDataModel

file_choice_field = [
    ("import", "Import"),
    ("export", "Export")
]

search_choice_field = [
    ("hs_code", "HS code"),
    ("hs_description", "HS Description"),
    ("product", "Product"),
    ("exporter_name", "Exporter Name"),
    ("importer_name", "Exporter Name"),
    ("iec_code", "IEC code")
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
        fields = ('id', 'hs_code', 'description')


class CompanyMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMaster
        fields = ('id', 'iec_code', 'name')


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


class FilterDataSerializer(serializers.ModelSerializer):
    data_type = fields.ChoiceField(
        choices=file_choice_field,
        required=True
    )
    country = serializers.IntegerField(
        required=True,
        allow_null=False
    )
    start_date = serializers.DateField(
        required=True,
        input_formats=["%Y-%m-%d"]
    )
    end_date = serializers.DateField(
        required=True,
        input_formats=["%Y-%m-%d"]
    )
    search_field = fields.ChoiceField(
        choices=search_choice_field,
        required=True
    )
    search_value = serializers.ListField(
        required=True
    )

    class Meta:
        model = FilterDataModel
        fields = ('data_type', 'country', 'start_date', 'end_date', 'search_field', 'search_value')


class AddWorkSpaceSerializer(serializers.ModelSerializer):
    search_id = serializers.IntegerField(
        required=True,
        allow_null=False
    )
    workspace_name = serializers.CharField(
        required=True,
        allow_null=False
    )

    def validate_search_id(self, search_id):
        if not FilterDataModel.objects.filter(id=search_id):
            raise serializers.ValidationError("Invalid search id")
        return search_id

    class Meta:
        model = FilterDataModel
        fields = ('search_id', 'workspace_name')


class WorkSpaceSerializer(serializers.ModelSerializer):
    workspace_name = serializers.CharField(
        required=False,
        allow_null=True
    )
    search_id = serializers.SerializerMethodField()

    def get_search_id(self, obj):
        return obj.id

    class Meta:
        model = FilterDataModel
        fields = ('search_id', 'workspace_name', 'tenant', 'data_type', 'country', 'start_date', 'end_date',
                  'search_field', 'search_value', 'is_active'
                  )


class WorkSpacePatchSerializer(serializers.ModelSerializer):
    search_id = serializers.SerializerMethodField()

    def get_search_id(self, obj):
        return obj.id

    class Meta:
        model = FilterDataModel
        fields = ('search_id', 'workspace_name', 'tenant', 'data_type', 'country', 'start_date', 'end_date',
                  'search_field', 'search_value', 'is_active')

        extra_kwargs = {
            'id': {'read_only': True},
            'tenant': {'read_only': True},
            'data_type': {'read_only': True},
            'country': {'read_only': True},
            'start_date': {'read_only': True},
            'end_date': {'read_only': True},
            'search_field': {'read_only': True},
            'search_value': {'read_only': True}
        }




