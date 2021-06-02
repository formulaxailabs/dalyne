import os
import uuid
import xlrd

from core_module.models import Plans, ImportTable, \
    CountryMaster, ExportTable, ProductMaster, \
    CompanyMaster, FilterDataModel, Tenant
from custom_decorator import response_modify_decorator_get_after_execution
from dalyne.settings import MEDIA_URL
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django_filters import rest_framework as djfilters
from drf_yasg.utils import swagger_auto_schema
from import_export.serializers import ProductMasterSerializer, CompanyMasterSerializer, ProductImportSerializer, \
    CompanyImportSerializer, \
    ExportImportUploadSerializer, CountryListSerializer, FilterDataSerializer, ImporterDataFilterSerializer, \
    ExporterDataFilterSerializer, WorkSpaceSerializer, AddWorkSpaceSerializer, WorkSpacePatchSerializer
from rest_framework import status, filters, exceptions, generics, viewsets, views
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from import_export.tasks import upload_excel_file_async, upload_company_file_async
from datetime import datetime

class PlansListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @response_modify_decorator_get_after_execution
    def get(self, request, *args, **kwargs):
        data = {}
        plans_data = Plans.objects.filter(is_deleted=False).values()
        data['features'] = [
            'Package Validity',
            'Download Points',
            'Unlimited Data Acecess',
            'Workspaces',
            'Searches',
            'Workspaces Validity',
            'Workspaces Deletion ( Per Qtr.)',
            'Shipment limit in Workspaces',
            'Add-On Points Facility',
            'Hot Products',
            'Hot Companies',
            'User',
        ]
        data['plans_list'] = plans_data

        return Response(data)


class ExcelDataImportView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ExportImportUploadSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            country_id = serializer.validated_data['country_id']
            file_name = serializer.validated_data['file'].name
            file = serializer.validated_data['file']
            fs = FileSystemStorage('media/import_export/')
            file_extension = file_name.split('.')[1].lower()
            filename = fs.save(
                file_name.split('.')[0].lower() + '_' + str(str(uuid.uuid4())[-4:]) + '.' + file_extension, file
            )
            full_path = f"{fs.location}/{filename}"
            print(f"Full Path {full_path}")
            file_extension = file_name.split('.')[1].lower()
            if file_extension == 'xls' or file_extension == 'xlsx':
                upload_excel_file_async.run(
                    country_id=country_id, user_id=self.request.user.id,
                    full_path=full_path, data_type=serializer.validated_data['type_of_sheet']
                )
                return Response(
                    {'msg': 'Your file will be uploaded shortly to our db'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': f"Only Files with 'xls' and 'xlsx are supported"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductDataImportAPI(generics.CreateAPIView):
    serializer_class = ProductImportSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file_name = serializer.validated_data['products_file'].name
            fs = FileSystemStorage('media/import_export/')
            file_extension = file_name.split('.')[1].lower()
            filename = fs.save(
                file_name.split('.')[0].lower() + '_' + str(str(uuid.uuid4())[-4:]) + '.' + file_extension,
                serializer.validated_data.get('products_file'))
            file_path = MEDIA_URL + 'import_export/' + filename
            cwd = os.getcwd()
            full_path = f"{cwd}/{file_path}"

            if file_extension == 'xls' or file_extension == 'xlsx':
                try:
                    book = xlrd.open_workbook(full_path)
                    sheet_obj = book.sheet_by_index(0)
                    max_rows = sheet_obj.nrows
                    products_list = list()
                    for rows_count in range(1, max_rows):
                        products_list.append(ProductMaster(
                            hs_code=sheet_obj.cell_value(rows_count, 0),
                            description=sheet_obj.cell_value(rows_count, 1),
                            created_by=self.request.user
                        ))
                    ProductMaster.objects.bulk_create(products_list)
                    return Response({
                        'msg': 'Product file gets successfully uploaded'},
                        status=status.HTTP_200_OK
                    )

                except xlrd.biffh.XLRDError:
                    return Response({
                        'error': 'Could not process the uploaded file at this moment'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': f"Only Files with 'xls' and 'xlsx are supported"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CompanyDataImportAPI(generics.CreateAPIView):
    serializer_class = CompanyImportSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file_name = serializer.validated_data['company_file'].name
            company_file = serializer.validated_data['company_file']
            file_extension = file_name.split('.')[1].lower()
            if file_extension == 'xls' or file_extension == 'xlsx':
                upload_company_file_async.run(
                    file_name=file_name,
                    company_file=company_file,
                    user_id=self.request.user.id
                )
                return Response({
                    'msg': 'Your file will be uploaded shortly to our db'},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {'error': f"Only Files with 'xls' and 'xlsx are supported"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CountriesListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CountryListSerializer

    def get_queryset(self):
        return CountryMaster.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        """ custom list method """
        if request.query_params.get('remove_pagination'):
            self.pagination_class = None
        return super(CountriesListAPI, self).list(request, *args, **kwargs)


class ProductListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductMasterSerializer
    filter_backends = (djfilters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       )
    search_fields = ('description',)

    def get_queryset(self):
        hs_code = self.request.query_params.get('hs_code')
        if hs_code:
            queryset = ProductMaster.objects.filter(is_deleted=False,
                                                    hs_code__istartswith=hs_code).order_by('hs_code')
        else:
            queryset = ProductMaster.objects.filter(is_deleted=False).order_by('hs_code')
        return queryset

    def list(self, request, *args, **kwargs):
        """ custom list method """
        if request.query_params.get('remove_pagination'):
            self.pagination_class = None
        return super(ProductListAPI, self).list(request, *args, **kwargs)


class CompanyListAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanyMasterSerializer
    filter_backends = (djfilters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       )
    search_fields = ('name', 'iec_code')
    model = CompanyMaster

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        """ custom list method """
        if request.query_params.get('remove_pagination'):
            self.pagination_class = None
        return super(CompanyListAPI, self).list(request, *args, **kwargs)


class AdvancedSearchAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (djfilters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       )
    model = FilterDataModel
    serializer_class = FilterDataSerializer

    @swagger_auto_schema(
        request_body=FilterDataSerializer,
        operation_id="Advanced Search")
    def create(self, request, *args, **kwargs):
        request_serializer = self.serializer_class(data=self.request.data)
        if request_serializer.is_valid(raise_exception=True):
            country_id = request_serializer.validated_data.pop("country")
            search_obj = request_serializer.save()
            country_obj = CountryMaster.objects.get(id=country_id)
            tenant = self.request.user.tenant
            search_obj.country = country_obj
            search_obj.tenant = tenant
            search_obj.save()
            resp_dict = dict()
            country = country_id
            start_date = request_serializer.validated_data.get("start_date")
            end_date = request_serializer.validated_data.get("end_date")
            search_field = request_serializer.validated_data.get("search_field")
            search_value = request_serializer.validated_data.get("search_value")

            if request_serializer.validated_data.get("data_type") == "export":
                model = ExportTable
                queryset = model.objects.filter(COUNTRY__id=country, SB_DATE__date__gte=start_date,
                                                SB_DATE__date__lte=end_date)
            else:
                model = ImportTable
                queryset = model.objects.filter(COUNTRY__id=country, BE_DATE__date__gte=start_date,
                                                BE_DATE__date__lte=end_date)
            if search_field == "hs_code":
                queryset = queryset.filter(Q(TWO_DIGIT__in=search_value) |
                                           Q(FOUR_DIGIT__in=search_value) |
                                           Q(RITC__in=search_value))
            if search_field == "importer_name":
                queryset = queryset.filter(IMPORTER_NAME__in=search_value)
            if search_field == "exporter_name":
                queryset = queryset.filter(EXPORTER_NAME__in=search_value)
            if search_field == "product":
                product_qs = ProductMaster.objects.filter(description__in=search_value)
                hs_code_list = list()
                for obj in product_qs:
                    hs_code_list.append(obj.hs_code)
                queryset = queryset.filter(Q(TWO_DIGIT__in=hs_code_list) |
                                           Q(FOUR_DIGIT__in=hs_code_list) |
                                           Q(RITC__in=hs_code_list))
            if search_field == "hs_description":
                initial_queryset = model.objects.none()
                for value in search_value:
                    initial_queryset = initial_queryset | queryset.filter(RITC_DISCRIPTION__icontains=value)
                queryset = initial_queryset
            if search_field == "iec_code":
                if model == ExportTable:
                    queryset = queryset.filter(EXPORTER_ID__in=search_value)
                if model == ImportTable:
                    queryset = queryset.filter(IMPORTER_ID__in=search_value)

            resp_dict["shipment_count"] = queryset.count()
            resp_dict["importer_count"] = queryset.distinct("IMPORTER_NAME").count()
            resp_dict["exporter_count"] = queryset.distinct("EXPORTER_NAME").count()
            resp_dict["country_origin"] = queryset.distinct("COUNTRY_OF_ORIGIN").count()
            resp_dict["port_of_destination"] = queryset.distinct("PORT_OF_DISCHARGE").count()
            resp_dict["hs_code_count"] = queryset.distinct("RITC").count()
            search_obj.total_count = resp_dict
            search_obj.save()
            resp_dict["search_id"] = search_obj.id
            return Response(
                resp_dict,
                status=status.HTTP_201_CREATED
            )
        else:
            raise exceptions.ValidationError(
                request_serializer.error
            )


class WorkSpaceAPI(viewsets.ModelViewSet):
    filter_backends = (djfilters.DjangoFilterBackend,
                       filters.SearchFilter,
                       )
    search_fields = ('workspace_name',)
    model = FilterDataModel
    http_method_names = ('get', 'post', 'patch', 'destroy')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WorkSpaceSerializer
        if self.request.method == 'POST':
            return AddWorkSpaceSerializer
        if self.request.method == 'PATCH':
            return WorkSpacePatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            search_id = serializer.validated_data.pop('search_id')
            search_obj = FilterDataModel.objects.filter(id=search_id).first()
            search_obj.workspace_name = serializer.validated_data.get('workspace_name')
            search_obj.save()
            return Response({'msg': 'Query successfully saved'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, instance=instance, partial=partial)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deactivate_workspace()
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteDuplicateCompaniesAPI(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            for obj in CompanyMaster.objects.values_list('iec_code', flat=True).distinct():
                CompanyMaster.objects.filter(pk__in=CompanyMaster.objects.filter(
                    iec_code=obj).values_list('id', flat=True)[1:]).delete()
            return Response({'msg': 'Successfully deleted'})
        except Exception as e:
            return Response({'error': e.args[0]})


class DeleteExportTableAPI(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            ExportTable.objects.all().delete()
            CompanyMaster.objects.all().delete()
            return Response({'msg': 'Successfully deleted'})
        except Exception as e:
            return Response({'error': e.args[0]})


class CurrentDateCompanyData(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            ExportTable.objects.filter(created_at__date=datetime.today()).delete()
            CompanyMaster.objects.filter(created_at__date=datetime.today()).delete()
            return Response({'msg': 'Successfully deleted'})
        except Exception as e:
            return Response({'error': e.args[0]})