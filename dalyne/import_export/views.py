import uuid
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from core_module.models import Profile, User, Plans, ImportTable, \
    CurrencyMaster, CountryMaster, ExportTable, ProductMaster, \
    CompanyMaster
from rest_framework.exceptions import APIException
from datetime import datetime
import time
from django.core.files.storage import FileSystemStorage
from import_export.serializers import ExcelDataImportSerializer, \
    PlansListSerializer, ImportViewSerializer, ExportViewSerializer, \
    ProductMasterSerializer, CompanyMasterSerializer, ProductImportSerializer, CompanyImportSerializer, \
    ExportImportUploadSerializer, CountryListSerializer
from dalyne.settings import MEDIA_URL
import xlrd
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
from django.core.paginator import Paginator
import json
import os
from custom_decorator import response_modify_decorator_post, \
    response_modify_decorator_get_after_execution, \
    response_decorator_list_or_get_after_execution_onoff_pagination, \
    response_modify_decorator_update
from django.db.models import Q


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
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ExportImportUploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            country_obj = CountryMaster.objects.get(id=serializer.validated_data['country_id'])
            file_name = serializer.validated_data['file'].name
            fs = FileSystemStorage('media/import_export/')
            file_extension = file_name.split('.')[1].lower()
            filename = fs.save(
                file_name.split('.')[0].lower() + '_' + str(str(uuid.uuid4())[-4:]) + '.' + file_extension,
                serializer.validated_data.get('file'))
            file_path = MEDIA_URL + 'import_export/' + filename
            cwd = os.getcwd()
            full_path = f"{cwd}{file_path}"
            if file_extension == 'xls' or file_extension == 'xlsx':
                try:
                    book = xlrd.open_workbook(full_path)
                    sheet_obj = book.sheet_by_index(0)
                    max_rows = sheet_obj.nrows
                    company_data = list()

                    if serializer.validated_data['type_of_sheet'] == 'export':
                        export_data = list()
                        for rowsCount in range(1, max_rows):
                            export_data.append(ExportTable(
                                SB_DATE=xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount, 1),
                                                                       book.datemode).strftime('%Y-%m-%d %H:%M:%S'),
                                MONTH=sheet_obj.cell_value(rowsCount, 2),
                                YEAR=sheet_obj.cell_value(rowsCount, 3),
                                RITC=sheet_obj.cell_value(rowsCount, 4),
                                TWO_DIGIT=sheet_obj.cell_value(rowsCount, 5),
                                FOUR_DIGIT=sheet_obj.cell_value(rowsCount, 6),
                                RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount, 7),
                                UQC=sheet_obj.cell_value(rowsCount, 8),
                                QUANTITY=sheet_obj.cell_value(rowsCount, 9),
                                CURRENCY=sheet_obj.cell_value(rowsCount, 10),
                                UNT_PRICE_FC=sheet_obj.cell_value(rowsCount, 11),
                                INV_VALUE_FC=sheet_obj.cell_value(rowsCount, 12),
                                UNT_PRICE_INR=sheet_obj.cell_value(rowsCount, 13),
                                INVOICE_NO=sheet_obj.cell_value(rowsCount, 14),
                                SB_NO=sheet_obj.cell_value(rowsCount, 15),
                                UNIT_RATE_WITH_FOB=sheet_obj.cell_value(rowsCount, 16),
                                PER_UNT_FOB=sheet_obj.cell_value(rowsCount, 17),
                                FOB_INR=sheet_obj.cell_value(rowsCount, 18),
                                FOB_FC=sheet_obj.cell_value(rowsCount, 19),
                                FOB_USD=sheet_obj.cell_value(rowsCount, 20),
                                EXCHANGE_RATE=sheet_obj.cell_value(rowsCount, 21),
                                IMPORTER_NAME=sheet_obj.cell_value(rowsCount, 22),
                                IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 23),
                                COUNTRY_OF_ORIGIN=sheet_obj.cell_value(rowsCount, 23),
                                PORT_OF_LOADING=sheet_obj.cell_value(rowsCount, 25),
                                PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount, 26),
                                PORT_CODE=sheet_obj.cell_value(rowsCount, 27),
                                MODE_OF_PORT=sheet_obj.cell_value(rowsCount, 28),
                                EXPORTER_ID=sheet_obj.cell_value(rowsCount, 29),
                                EXPORTER_NAME=sheet_obj.cell_value(rowsCount, 30),
                                EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 31),
                                EXPORTER_CITY=sheet_obj.cell_value(rowsCount, 32),
                                EXPORTER_STATE=sheet_obj.cell_value(rowsCount, 33),
                                EXPORTER_PIN=sheet_obj.cell_value(rowsCount, 34),
                                EXPORTER_PHONE=sheet_obj.cell_value(rowsCount, 35),
                                EXPORTER_EMAIL=sheet_obj.cell_value(rowsCount, 36),
                                EXPORTER_CONTACT_PERSON=sheet_obj.cell_value(rowsCount, 37),
                                COUNTRY=country_obj,
                                created_by=self.request.user
                            )
                            )
                            company_name = sheet_obj.cell_value(rowsCount, 30)
                            iec_code = sheet_obj.cell_value(rowsCount, 29)
                            if not CompanyMaster.objects.filter(Q(name=company_name) | Q(iec_code=iec_code)):
                                if iec_code in [None, '']:
                                    iec_code = f"DALYNE{(str(uuid.uuid4())[-4:])}"
                                company_data.append(CompanyMaster(
                                    name=sheet_obj.cell_value(rowsCount, 30),
                                    iec_code=iec_code,
                                    created_by=self.request.user

                                )
                                )
                        ExportTable.objects.bulk_create(export_data)
                        CompanyMaster.objects.bulk_create(company_data)
                        return Response({
                            'msg': 'Exporter Data file gets successfully uploaded'},
                            status=status.HTTP_200_OK
                        )

                    elif serializer.validated_data['type_of_sheet'] == 'import':
                        import_data = list()
                        for rowsCount in range(1, max_rows):
                            import_data.append(ImportTable(
                                BE_DATE=xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount, 1),
                                                                       book.datemode).strftime('%Y-%m-%d %H:%M:%S'),
                                MONTH=sheet_obj.cell_value(rowsCount, 2),
                                YEAR=sheet_obj.cell_value(rowsCount, 3),
                                RITC=sheet_obj.cell_value(rowsCount, 4),
                                TWO_DIGIT=sheet_obj.cell_value(rowsCount, 5),
                                FOUR_DIGIT=sheet_obj.cell_value(rowsCount, 6),
                                RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount, 7),
                                UQC=sheet_obj.cell_value(rowsCount, 8),
                                QUANTITY=sheet_obj.cell_value(rowsCount, 9),
                                CURRENCY=sheet_obj.cell_value(rowsCount, 10),
                                UNT_PRICE_FC=sheet_obj.cell_value(rowsCount, 11),
                                INV_VALUE_FC=sheet_obj.cell_value(rowsCount, 12),
                                UNT_PRICE_INR=sheet_obj.cell_value(rowsCount, 13),
                                INV_NO=sheet_obj.cell_value(rowsCount, 14),
                                BE_NO=sheet_obj.cell_value(rowsCount, 15),
                                UNT_RATE_WITH_DUTY=sheet_obj.cell_value(rowsCount, 16),
                                PER_UNT_DUTY=sheet_obj.cell_value(rowsCount, 17),
                                DUTY_INR=sheet_obj.cell_value(rowsCount, 18),
                                DUTY_FC=sheet_obj.cell_value(rowsCount, 19),
                                DUTY_PERCENT=sheet_obj.cell_value(rowsCount, 20),
                                EX_TOTAL_VALUE=sheet_obj.cell_value(rowsCount, 21),
                                ASS_VALUE_INR=sheet_obj.cell_value(rowsCount, 22),
                                ASS_VALUE_USD=sheet_obj.cell_value(rowsCount, 23),
                                ASS_VALUE_FC=sheet_obj.cell_value(rowsCount, 24),
                                EXCHANGE_RATE=sheet_obj.cell_value(rowsCount, 25),
                                EXPORTER_NAME=sheet_obj.cell_value(rowsCount, 26),
                                EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 27),
                                COUNTRY_OF_ORIGIN=sheet_obj.cell_value(rowsCount, 28),
                                PORT_OF_LOADING=sheet_obj.cell_value(rowsCount, 29),
                                PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount, 30),
                                PORT_CODE=sheet_obj.cell_value(rowsCount, 31),
                                MODE_OF_PORT=sheet_obj.cell_value(rowsCount, 32),
                                IMPORTER_ID=sheet_obj.cell_value(rowsCount, 33),
                                IMPORTER_NAME=sheet_obj.cell_value(rowsCount, 34),
                                IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount, 35),
                                IMPORTER_CITY_STATE=sheet_obj.cell_value(rowsCount, 36),
                                IMPORTER_PIN=sheet_obj.cell_value(rowsCount, 37),
                                IMPORTER_PHONE=sheet_obj.cell_value(rowsCount, 38),
                                IMPORTER_EMAIL=sheet_obj.cell_value(rowsCount, 39),
                                IMPORTER_CONTACT_PERSON=sheet_obj.cell_value(rowsCount, 40),
                                BE_TYPE=sheet_obj.cell_value(rowsCount, 41),
                                CHA_NAME=sheet_obj.cell_value(rowsCount, 42),
                                Item_No=sheet_obj.cell_value(rowsCount, 43),
                                COUNTRY=country_obj,
                                created_by=self.request.user
                            )
                            )
                            company_name = sheet_obj.cell_value(rowsCount, 34)
                            iec_code = sheet_obj.cell_value(rowsCount, 33)

                            if not CompanyMaster.objects.filter(Q(name=company_name) | Q(iec_code=iec_code)):
                                iec_code = sheet_obj.cell_value(rowsCount, 33)
                                if iec_code in [None, '']:
                                    iec_code = f"DALYNE{(str(uuid.uuid4())[-4:])}"
                                company_data.append(CompanyMaster(
                                    name=sheet_obj.cell_value(rowsCount, 34),
                                    iec_code=iec_code,
                                    created_by=self.request.user

                                )
                                )
                        ImportTable.objects.bulk_create(import_data)
                        CompanyMaster.objects.bulk_create(company_data)

                        return Response({
                            'msg': 'Importer Data file gets successfully uploaded'},
                            status=status.HTTP_200_OK
                        )
                except Exception as e:
                    print(e.__str__())
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


class ImportExportListView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = LimitOffsetPagination

    def get(self, request):
        PageExists = False
        total_record = 0
        limit = request.GET.get('limit', settings.PAGINATION_LIMIT)
        page = request.GET.get('page', settings.PAGINATION_OFFSET)
        result = []
        response = {}
        search_key = request.GET.get('q', "")
        order_by_querystring = request.GET.get('order_by')
        columnname_querystring = request.GET.get('colname')
        data_type = request.GET.get('data_type', 'import')
        country = request.GET.get('country')
        filter_params = request.GET.get('filter_params', [])
        type_str = ""
        and_filter = {}
        filter_params = json.loads(filter_params) if filter_params else []

        if len(filter_params) > 0:
            for param in filter_params:
                print(param)
                and_filter[param['field'] + "__" + param['condition']] = param['value']

        if data_type == 'import':
            queryset = ImportTable.objects.filter(COUNTRY_OF_ORIGIN_id=country, **and_filter)
            type_str = "Import"
        else:
            queryset = ExportTable.objects.filter(COUNTRY_OF_ORIGIN_id=country, **and_filter)
            type_str = "Export"

        if queryset.count() > 0:
            if limit is None or limit == '' or str(limit) == str(0):
                limit = queryset.count()
            if page is None or page is '' or page is 0:
                page = 1

            record_size = int(limit)
            paginator = Paginator(queryset, int(record_size))
            total_record = paginator.count
            all_data = paginator.get_page(page)
            all_data = all_data.object_list
            try:
                PageExists = paginator.page(page)
            except InvalidPage:
                PageExists = False

            if PageExists:
                # paginator = LimitOffsetPagination()
                # result_page = paginator.paginate_queryset(queryset,request)
                if data_type == 'import':
                    serializer_class = ImportViewSerializer(all_data, many=True)
                else:
                    serializer_class = ExportViewSerializer(all_data, many=True)
                result = serializer_class.data

                response = {'status_code': status.HTTP_200_OK, "message": type_str + " Records", "result": result,
                            "RecordsCount": total_record}
            else:
                response = {"status_code": status.HTTP_200_OK, "message": "No data found!", "result": [],
                            "RecordsCount": total_record}

        else:
            response = {"status_code": status.HTTP_200_OK, "message": "No data found!", "result": [], "RecordsCount": 0}
        return Response(response)


class ProductFilterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        response = {}
        dataresult = []

        search_value = request.GET.get('search_value', "")
        if search_value != "":
            queryset = ProductMaster.objects.filter(is_deleted=False, description__icontains=search_value)
            serializer_class = ProductMasterSerializer(queryset, many=True)
            dataresult = serializer_class.data
            response = {'status_code': status.HTTP_200_OK, 'result': dataresult}
        else:
            response = {'status_code': status.HTTP_400_BAD_REQUEST, 'result': dataresult}
        return Response(response)


class CompanyFilterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        response = {}
        dataresult = []

        search_value = request.GET.get('search_value', "")
        if search_value != "":
            queryset = CompanyMaster.objects.filter(is_deleted=False, name__istartswith=search_value)
            serializer_class = CompanyMasterSerializer(queryset, many=True)
            dataresult = serializer_class.data
            response = {'status_code': status.HTTP_200_OK, 'result': dataresult}
        else:
            response = {'status_code': status.HTTP_400_BAD_REQUEST, 'result': dataresult}
        return Response(response)


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
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file_name = serializer.validated_data['company_file'].name
            fs = FileSystemStorage('media/import_export/')
            file_extension = file_name.split('.')[1].lower()
            filename = fs.save(
                file_name.split('.')[0].lower() + '_' + str(str(uuid.uuid4())[-4:]) + '.' + file_extension,
                serializer.validated_data.get('company_file'))
            file_path = MEDIA_URL + 'import_export/' + filename
            cwd = os.getcwd()
            full_path = f"{cwd}/{file_path}"

            if file_extension == 'xls' or file_extension == 'xlsx':
                try:
                    book = xlrd.open_workbook(full_path)
                    sheet_obj = book.sheet_by_index(0)
                    max_rows = sheet_obj.nrows
                    companies_list = list()
                    for rows_count in range(1, max_rows):
                        companies_list.append(CompanyMaster(
                            name=sheet_obj.cell_value(rows_count, 0),
                            iec_code=sheet_obj.cell_value(rows_count, 1),
                            created_by=self.request.user
                        ))
                    CompanyMaster.objects.bulk_create(companies_list)
                    return Response({
                        'msg': 'Company file gets successfully uploaded'},
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


class CountriesListAPI(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CountryListSerializer

    def get_queryset(self):
        return CountryMaster.objects.all()
