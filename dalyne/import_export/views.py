from django.shortcuts import render
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
from django.contrib.auth.signals import user_logged_out
# from import_export.serializers import
from rest_framework.exceptions import APIException
from datetime import datetime
import time
from django.core.files.storage import FileSystemStorage
from import_export.serializers import ExcelDataImportSerializer, \
    PlansListSerializer, ImportViewSerializer, ExportViewSerializer,\
    ProductMasterSerializer, CompanyMasterSerializer
from dalyne.settings import MEDIA_URL
import xlrd
from rest_framework.pagination import LimitOffsetPagination
from django.conf import settings
from django.core.paginator import Paginator
import json

class PlansListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self,request):
        response={}
        queryset = Plans.objects.filter(is_deleted=False)
        serializer_class = PlansListSerializer(queryset, many=True)
        dataresult=serializer_class.data

        response={'status_code': status.HTTP_200_OK,'result':dataresult}
        return Response(response)

class ExcelDataImportView(generics.CreateAPIView):
    """Create a new user in system"""
    permission_classes = [AllowAny]
    # queryset = ImportTable.objects.all()
    # serializer_class = ExcelDataImportSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, format=None):
        data = {"message":request.data.get('file_type')}
        file_type = request.data.get('file_type')
        uploaded_file = request.FILES['file_to_upload']
        fs = FileSystemStorage('media/import_export/')
        file_extenion = uploaded_file.name.split('.')[1].lower()
        millis = str(int(round(time.time() * 1000)))
        filename = fs.save(uploaded_file.name.split('.')[0].lower()+'_'+str(millis)+'.'+file_extenion,uploaded_file)
        uploaded_file_url = MEDIA_URL+'import_export/'+filename

        data['uploaded_file_url'] = uploaded_file_url

        EXCELDATAOBJECT=[]
        if uploaded_file.name.split(".")[1].lower() == 'xls' or uploaded_file.name.split(".")[1].lower() == 'xlsx':
            try:
                book = xlrd.open_workbook(uploaded_file_url)
            except xlrd.biffh.XLRDError:
                print("XLRDError occure")

            # book = xlrd.open_workbook(uploaded_file_url)
            sheet_obj= book.sheet_by_index(0)
            # max_cols=sheet_obj.ncols
            max_rows=sheet_obj.nrows
            # titleRows = sheet_obj.row_slice(0)
            # print("titleRows", titleRows)
            # all_fields =[f.name for f in ImportTable._meta.fields]
            # print("all_fields", all_fields)
            # for i in titleRows:
            #     print(i.value)
            #     break

            DATASET=[]
            if file_type=='import':
                for rowsCount in range(1,max_rows):
                    currency, created1 = CurrencyMaster.objects.get_or_create(name=sheet_obj.cell_value(rowsCount,10),is_deleted=False)
                    country, created2 = CountryMaster.objects.get_or_create(name=sheet_obj.cell_value(rowsCount,28),is_deleted=False)
                    DATASET.append(ImportTable(
                        BE_DATE=xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount,1), book.datemode).strftime('%Y-%m-%d %H:%M:%S'),
                        MONTH=sheet_obj.cell_value(rowsCount,2),
                        YEAR=sheet_obj.cell_value(rowsCount,3),
                        RITC=sheet_obj.cell_value(rowsCount,4),
                        TWO_DIGIT=sheet_obj.cell_value(rowsCount,5),
                        FOUR_DIGIT=sheet_obj.cell_value(rowsCount,6),
                        RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount,7),
                        UQC=sheet_obj.cell_value(rowsCount,8),
                        QUANTITY=sheet_obj.cell_value(rowsCount,9),
                        CURRENCY=currency,
                        UNT_PRICE_FC=sheet_obj.cell_value(rowsCount,11),
                        INV_VALUE_FC=sheet_obj.cell_value(rowsCount,12),
                        UNT_PRICE_INR=sheet_obj.cell_value(rowsCount,13),
                        INV_NO=sheet_obj.cell_value(rowsCount,14),
                        BE_NO=sheet_obj.cell_value(rowsCount,15),
                        UNT_RATE_WITH_DUTY=sheet_obj.cell_value(rowsCount,16),
                        PER_UNT_DUTY=sheet_obj.cell_value(rowsCount,17),
                        DUTY_INR=sheet_obj.cell_value(rowsCount,18),
                        DUTY_FC=sheet_obj.cell_value(rowsCount,19),
                        DUTY_PERCENT=sheet_obj.cell_value(rowsCount,20),
                        EX_TOTAL_VALUE=sheet_obj.cell_value(rowsCount,21),
                        ASS_VALUE_INR=sheet_obj.cell_value(rowsCount,22),
                        ASS_VALUE_USD=sheet_obj.cell_value(rowsCount,23),
                        ASS_VALUE_FC=sheet_obj.cell_value(rowsCount,24),
                        EXCHANGE_RATE=sheet_obj.cell_value(rowsCount,25),
                        EXPORTER_NAME=sheet_obj.cell_value(rowsCount,26),
                        EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount,27),
                        COUNTRY_OF_ORIGIN=country,
                        PORT_OF_LOADING=sheet_obj.cell_value(rowsCount,29),
                        PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount,30),
                        PORT_CODE=sheet_obj.cell_value(rowsCount,31),
                        MODE_OF_PORT=sheet_obj.cell_value(rowsCount,32),
                        IMPORTER_ID=sheet_obj.cell_value(rowsCount,33),
                        IMPORTER_NAME=sheet_obj.cell_value(rowsCount,34),
                        IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount,35),
                        IMPORTER_CITY_STATE=sheet_obj.cell_value(rowsCount,36),
                        IMPORTER_PIN=sheet_obj.cell_value(rowsCount,37),
                        IMPORTER_PHONE=sheet_obj.cell_value(rowsCount,38),
                        IMPORTER_EMAIL=sheet_obj.cell_value(rowsCount,39),
                        IMPORTER_CONTACT_PERSON=sheet_obj.cell_value(rowsCount,40),
                        BE_TYPE=sheet_obj.cell_value(rowsCount,41),
                        CHA_NAME=sheet_obj.cell_value(rowsCount,42),
                        Item_No=sheet_obj.cell_value(rowsCount,43),
                        )
                    )
                ImportTable.objects.bulk_create(DATASET)

                response = {
                    "message":"Import data saved.",
                    "status_code":status.HTTP_201_CREATED}
            
            elif file_type=='export':
                for rowsCount in range(1,max_rows):
                    currency, created1 = CurrencyMaster.objects.get_or_create(name=sheet_obj.cell_value(rowsCount,10),is_deleted=False)
                    country, created2 = CountryMaster.objects.get_or_create(name=sheet_obj.cell_value(rowsCount,24),is_deleted=False)
                    DATASET.append(ExportTable(
                        SB_DATE=xlrd.xldate.xldate_as_datetime(sheet_obj.cell_value(rowsCount,1), book.datemode).strftime('%Y-%m-%d %H:%M:%S'),
                        MONTH=sheet_obj.cell_value(rowsCount,2),
                        YEAR=sheet_obj.cell_value(rowsCount,3),
                        RITC=sheet_obj.cell_value(rowsCount,4),
                        TWO_DIGIT=sheet_obj.cell_value(rowsCount,5),
                        FOUR_DIGIT=sheet_obj.cell_value(rowsCount,6),
                        RITC_DISCRIPTION=sheet_obj.cell_value(rowsCount,7),
                        UQC=sheet_obj.cell_value(rowsCount,8),
                        QUANTITY=sheet_obj.cell_value(rowsCount,9),
                        CURRENCY=currency,
                        UNT_PRICE_FC=sheet_obj.cell_value(rowsCount,11),
                        INV_VALUE_FC=sheet_obj.cell_value(rowsCount,12),
                        UNT_PRICE_INR=sheet_obj.cell_value(rowsCount,13),
                        INVOICE_NO=sheet_obj.cell_value(rowsCount,14),
                        SB_NO=sheet_obj.cell_value(rowsCount,15),
                        UNIT_RATE_WITH_FOB=sheet_obj.cell_value(rowsCount,16),
                        PER_UNT_FOB=sheet_obj.cell_value(rowsCount,17),
                        FOB_INR=sheet_obj.cell_value(rowsCount,18),
                        FOB_FC=sheet_obj.cell_value(rowsCount,19),
                        FOB_USD=sheet_obj.cell_value(rowsCount,20),
                        EXCHANGE_RATE=sheet_obj.cell_value(rowsCount,21),
                        IMPORTER_NAME =sheet_obj.cell_value(rowsCount,22),
                        IMPORTER_ADDRESS=sheet_obj.cell_value(rowsCount,23),
                        COUNTRY_OF_ORIGIN=country,
                        PORT_OF_LOADING=sheet_obj.cell_value(rowsCount,25),
                        PORT_OF_DISCHARGE=sheet_obj.cell_value(rowsCount,26),
                        PORT_CODE=sheet_obj.cell_value(rowsCount,27),
                        MODE_OF_PORT=sheet_obj.cell_value(rowsCount,28),
                        EXPORTER_ID=sheet_obj.cell_value(rowsCount,29),
                        EXPORTER_NAME=sheet_obj.cell_value(rowsCount,30),
                        EXPORTER_ADDRESS=sheet_obj.cell_value(rowsCount,31),
                        EXPORTER_CITY=sheet_obj.cell_value(rowsCount,32),
                        EXPORTER_STATE=sheet_obj.cell_value(rowsCount,33),
                        EXPORTER_PIN=sheet_obj.cell_value(rowsCount,34),
                        EXPORTER_PHONE=sheet_obj.cell_value(rowsCount,35),
                        EXPORTER_EMAIL=sheet_obj.cell_value(rowsCount,36),
                        EXPORTER_CONTACT_PERSON=sheet_obj.cell_value(rowsCount,37),
                        )
                    )
                ExportTable.objects.bulk_create(DATASET)

                response = {
                    "message":"Export data saved.",
                    "status_code":status.HTTP_201_CREATED}
            
        return Response(response)


class ImportExportListView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = LimitOffsetPagination

    def get(self,request):
        PageExists=False
        total_record=0
        limit = request.GET.get('limit',settings.PAGINATION_LIMIT)
        page = request.GET.get('page',settings.PAGINATION_OFFSET)
        result=[]
        response={}
        search_key = request.GET.get('q',"")
        order_by_querystring = request.GET.get('order_by')
        columnname_querystring = request.GET.get('colname')
        data_type = request.GET.get('data_type', 'import')
        country = request.GET.get('country')
        filter_params = request.GET.get('filter_params',[])
        type_str = ""
        and_filter = {}
        filter_params = json.loads(filter_params) if filter_params else []

        if len(filter_params)>0:
            for param in filter_params:
                print(param)
                and_filter[param['field']+"__"+param['condition']] = param['value']


        if data_type=='import':
            queryset = ImportTable.objects.filter(COUNTRY_OF_ORIGIN_id=country,**and_filter)
            type_str = "Import"
        else:
            queryset = ExportTable.objects.filter(COUNTRY_OF_ORIGIN_id=country,**and_filter)
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
                if data_type=='import':
                    serializer_class = ImportViewSerializer(all_data,many=True)
                else:
                    serializer_class = ExportViewSerializer(all_data,many=True)
                result = serializer_class.data

                response={'status_code': status.HTTP_200_OK,"message": type_str+" Records","result":result,"RecordsCount":total_record}
            else:	
                response={"status_code":status.HTTP_200_OK,"message":"No data found!","result":[],"RecordsCount":total_record}

        else:	
            response={"status_code":status.HTTP_200_OK,"message":"No data found!","result":[],"RecordsCount":0}
        return Response(response)


class ProductFilterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self,request):
        response={}
        dataresult = []
        
        search_value = request.GET.get('search_value',"")
        if search_value!="":
            queryset = ProductMaster.objects.filter(is_deleted=False,description__icontains=search_value)
            serializer_class = ProductMasterSerializer(queryset, many=True)
            dataresult=serializer_class.data
            response={'status_code': status.HTTP_200_OK,'result':dataresult}
        else:
            response={'status_code': status.HTTP_400_BAD_REQUEST,'result':dataresult}
        return Response(response)


class CompanyFilterListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self,request):
        response={}
        dataresult = []
        
        search_value = request.GET.get('search_value',"")
        if search_value!="":
            queryset = CompanyMaster.objects.filter(is_deleted=False,name__istartswith=search_value)
            serializer_class = CompanyMasterSerializer(queryset, many=True)
            dataresult=serializer_class.data
            response={'status_code': status.HTTP_200_OK,'result':dataresult}
        else:
            response={'status_code': status.HTTP_400_BAD_REQUEST,'result':dataresult}
        return Response(response)