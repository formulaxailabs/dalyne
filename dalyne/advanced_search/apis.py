import xlwt
import uuid
from django_filters import rest_framework as djfilters
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics, permissions, exceptions, views, filters
from core_module.models import ImportTable, ExportTable, Plans, \
    ProductMaster, CompanyMaster, CountryMaster, FilterDataModel
from import_export.serializers import ImporterDataFilterSerializer, ExporterDataFilterSerializer
from .serializers import ExporterNameSerializer, ImporterNameSerializer

QUERY_LIMIT = 30000


class SubFilterListingAPI(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        search_id = self.request.query_params.get("search_id")
        search_obj = FilterDataModel.objects.filter(id=search_id).first()
        if search_obj:
            if search_obj.data_type == "export":
                return ExporterDataFilterSerializer
            elif search_obj.data_type == "import":
                return ImporterDataFilterSerializer
        else:
            return ImporterDataFilterSerializer

    def get_queryset(self):
        search_id = self.request.query_params.get('search_id')
        exporter = self.request.query_params.get('exporter', None)
        importer = self.request.query_params.get('importer', None)
        uqc = self.request.query_params.get('uqc', None)
        country_origin = self.request.query_params.get('country', None)
        port_of_discharge = self.request.query_params.get('port_of_discharge', None)
        port_of_loading = self.request.query_params.get('port_of_loading', None)
        mode = self.request.query_params.get('mode', None)
        port_code = self.request.query_params.get('port_code', None)
        hs_code = self.request.query_params.get('hs_code', None)
        description = self.request.query_params.get('description', None)
        min_qty = self.request.query_params.get('min_qty', None)
        max_qty = self.request.query_params.get('max_qty', None)
        if search_id:
            search_obj = FilterDataModel.objects.filter(id=search_id).first()
            if search_obj:
                country = search_obj.country.name
                start_date = search_obj.start_date
                end_date = search_obj.end_date
                search_field = search_obj.search_field
                search_value = search_obj.search_value
                data_type = search_obj.data_type
                if data_type == "export":
                    model = ExportTable
                    qs = model.objects.filter(COUNTRY__name=country, SB_DATE__date__gte=start_date,
                                              SB_DATE__date__lte=end_date)
                else:
                    model = ImportTable
                    qs = model.objects.filter(COUNTRY__name=country, BE_DATE__date__gte=start_date,
                                              BE_DATE__date__lte=end_date)
                if search_field == "hs_code":
                    qs = qs.filter(Q(TWO_DIGIT__in=search_value) |
                                   Q(FOUR_DIGIT__in=search_value) |
                                   Q(RITC__in=search_value))
                if search_field == "importer_name":
                    qs = qs.filter(IMPORTER_NAME__in=search_value)
                if search_field == "exporter_name":
                    qs = qs.filter(EXPORTER_NAME__in=search_value)
                if search_field == "product":
                    product_qs = ProductMaster.objects.filter(description__in=search_value)
                    hs_code_list = list()
                    for obj in product_qs:
                        hs_code_list.append(obj.hs_code)
                    qs = qs.filter(Q(TWO_DIGIT__in=hs_code_list) |
                                   Q(FOUR_DIGIT__in=hs_code_list) |
                                   Q(RITC__in=hs_code_list))
                if search_field == "hs_description":
                    initial_queryset = model.objects.none()
                    for value in search_value:
                        initial_queryset = initial_queryset | qs.filter(RITC_DISCRIPTION__icontains=value)
                    qs = initial_queryset
                if search_field == "iec_code":
                    if model == ExportTable:
                        qs = qs.filter(EXPORTER_ID__in=search_value)
                    if model == ImportTable:
                        qs = qs.filter(IMPORTER_ID__in=search_value)
                if exporter:
                    if model == ExportTable:
                        qs = qs.filter(Q(EXPORTER_ID__icontains=exporter) |
                                       Q(EXPORTER_NAME__icontains=exporter))
                    if model == ImportTable:
                        qs = qs.filter(EXPORTER_NAME__icontains=exporter)
                if importer:
                    if model == ExportTable:
                        qs = qs.filter(IMPORTER_NAME__icontains=importer)
                    if model == ImportTable:
                        qs = qs.filter(Q(IMPORTER_NAME__icontains=importer) |
                                       Q(IMPORTER_ID__icontains=importer))

                if uqc:
                    qs = qs.filter(UQC__icontains=uqc)
                if country_origin:
                    qs = qs.filter(COUNTRY_OF_ORIGIN__icontains=country_origin)
                if port_of_loading:
                    qs = qs.filter(PORT_OF_LOADING__icontains=port_of_loading)
                if port_of_discharge:
                    qs = qs.filter(PORT_OF_DISCHARGE__icontains=port_of_discharge)
                if mode:
                    qs = qs.filter(MODE_OF_PORT__icontains=mode)
                if port_code:
                    qs = qs.filter(PORT_CODE__icontains=port_code)
                if description:
                    qs = qs.filter(RITC_DISCRIPTION__icontains=description)
                if hs_code:
                    qs = qs.filter(RITC__icontains=hs_code)
                if min_qty or max_qty:
                    if (min_qty and not max_qty) or (max_qty and not min_qty):
                        raise exceptions.ValidationError("Both min quantity and max quantity are required")
                    else:
                        qs = qs.filter(QUANTITY__gte=min_qty, QUANTITY__lte=max_qty)
                return qs
            else:
                return {}
        else:
            return {}

    def list(self, request, *args, **kwargs):
        """ custom list method """
        if request.query_params.get('remove_pagination'):
            self.pagination_class = None
        return super(SubFilterListingAPI, self).list(request, *args, **kwargs)


class ExportAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_model_name(self):
        search_id = self.request.query_params.get("search_id")
        search_obj = FilterDataModel.objects.filter(id=search_id).first()
        if search_obj.data_type == "export":
            return ExportTable
        else:
            return ImportTable

    def write_header(self, sheet, header):
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for index, header_value in enumerate(header):
            sheet.write(0, index, header_value, font_style)

        return sheet

    def get_queryset(self):
        search_id = self.request.query_params.get('search_id')
        exporter = self.request.query_params.get('exporter', None)
        importer = self.request.query_params.get('importer', None)
        uqc = self.request.query_params.get('uqc', None)
        country_origin = self.request.query_params.get('country', None)
        port_of_discharge = self.request.query_params.get('port_of_discharge', None)
        port_of_loading = self.request.query_params.get('port_of_loading', None)
        mode = self.request.query_params.get('mode', None)
        port_code = self.request.query_params.get('port_code', None)
        hs_code = self.request.query_params.get('hs_code', None)
        description = self.request.query_params.get('description', None)
        min_qty = self.request.query_params.get('min_qty', None)
        max_qty = self.request.query_params.get('max_qty', None)
        if search_id:
            search_obj = FilterDataModel.objects.filter(id=search_id).first()
            if search_obj:
                country = search_obj.country.name
                start_date = search_obj.start_date
                end_date = search_obj.end_date
                search_field = search_obj.search_field
                search_value = search_obj.search_value
                data_type = search_obj.data_type
                if data_type == "export":
                    model = ExportTable
                    qs = model.objects.filter(COUNTRY__name=country, SB_DATE__date__gte=start_date,
                                              SB_DATE__date__lte=end_date)
                else:
                    model = ImportTable
                    qs = model.objects.filter(COUNTRY__name=country, BE_DATE__date__gte=start_date,
                                              BE_DATE__date__lte=end_date)
                if search_field == "hs_code":
                    qs = qs.filter(Q(TWO_DIGIT__in=search_value) |
                                   Q(FOUR_DIGIT__in=search_value) |
                                   Q(RITC__in=search_value))
                if search_field == "importer_name":
                    qs = qs.filter(IMPORTER_NAME__in=search_value)
                if search_field == "exporter_name":
                    qs = qs.filter(EXPORTER_NAME__in=search_value)
                if search_field == "product":
                    product_qs = ProductMaster.objects.filter(description__in=search_value)
                    hs_code_list = list()
                    for obj in product_qs:
                        hs_code_list.append(obj.hs_code)
                    qs = qs.filter(Q(TWO_DIGIT__in=hs_code_list) |
                                   Q(FOUR_DIGIT__in=hs_code_list) |
                                   Q(RITC__in=hs_code_list))
                if search_field == "hs_description":
                    initial_queryset = model.objects.none()
                    for value in search_value:
                        initial_queryset = initial_queryset | qs.filter(RITC_DISCRIPTION__icontains=value)
                    qs = initial_queryset
                if search_field == "iec_code":
                    if model == ExportTable:
                        qs = qs.filter(EXPORTER_ID__in=search_value)
                    if model == ImportTable:
                        qs = qs.filter(IMPORTER_ID__in=search_value)
                if exporter:
                    if model == ExportTable:
                        qs = qs.filter(Q(EXPORTER_ID__icontains=exporter) |
                                       Q(EXPORTER_NAME__icontains=exporter))
                    if model == ImportTable:
                        qs = qs.filter(EXPORTER_NAME__icontains=exporter)
                if importer:
                    if model == ExportTable:
                        qs = qs.filter(IMPORTER_NAME__icontains=importer)
                    if model == ImportTable:
                        qs = qs.filter(Q(IMPORTER_NAME__icontains=importer) |
                                       Q(IMPORTER_ID__icontains=importer))

                if uqc:
                    qs = qs.filter(UQC__icontains=uqc)
                if country_origin:
                    qs = qs.filter(COUNTRY_OF_ORIGIN__icontains=country_origin)
                if port_of_loading:
                    qs = qs.filter(PORT_OF_LOADING__icontains=port_of_loading)
                if port_of_discharge:
                    qs = qs.filter(PORT_OF_DISCHARGE__icontains=port_of_discharge)
                if mode:
                    qs = qs.filter(MODE_OF_PORT__icontains=mode)
                if port_code:
                    qs = qs.filter(PORT_CODE__icontains=port_code)
                if description:
                    qs = qs.filter(RITC_DISCRIPTION__icontains=description)
                if hs_code:
                    qs = qs.filter(RITC__icontains=hs_code)
                if min_qty or max_qty:
                    if (min_qty and not max_qty) or (max_qty and not min_qty):
                        raise exceptions.ValidationError("Both min quantity and max quantity are required")
                    else:
                        qs = qs.filter(QUANTITY__gte=min_qty, QUANTITY__lte=max_qty)
                return qs
        else:
            raise exceptions.ValidationError("Search id is required")

    def get(self, request, *args, **kwargs):
        excel_limit = QUERY_LIMIT
        model = self.get_model_name()
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'
        if model == ExportTable:
            response = HttpResponse(content_type='application/ms-excel')
            filename = "Exporters_" + "shipments" + "_" + str(uuid.uuid4())[-4:] + ".xls"

            response['Content-Disposition'] = f'attachment; filename={filename}'

            header = ['S.No', 'TYPE', 'COUNTRY', 'DATE', 'MONTH', 'YEAR', 'HS CODE', 'TWO DIGIT', 'FOUR DIGIT',
                      'HS CODE DESCRIPTION', 'COMMODITY DESCRIPTION', 'UNIT', 'QUANTITY', 'CURRENCY',
                      'UNT PRICE_FC', 'INV VALUE_FC', 'INV VALUE_INR', 'INVOICE NUMBER', 'SB NUMBER',
                      'UNIT RATE WITH FOB', 'PER UNT FOB', 'FOB INR', 'FOB FC', 'FOB USD', 'EXCHANGE RATE',
                      'IMPORTER NAME', 'IMPORTER ADDRESS', 'COUNTRY OF ORIGIN', 'PORT OF LOADING', 'PORT OF DISCHARGE',
                      'PORT CODE', 'MODE OF PORT', 'IEC', 'EXPORTER NAME', 'EXPORTER ADDRESS', 'EXPORTER CITY',
                      'EXPORTER PIN']

            fields = ['COUNTRY', 'SB_DATE', 'MONTH', 'YEAR', 'RITC', 'TWO_DIGIT', 'FOUR_DIGIT', 'RITC_DISCRIPTION',
                      'commodity_description', 'UQC', 'QUANTITY', 'CURRENCY', 'UNT_PRICE_FC', 'INV_VALUE_FC',
                      'UNT_PRICE_INR', 'INVOICE_NO', 'SB_NO', 'UNIT_RATE_WITH_FOB', 'PER_UNT_FOB', 'FOB_INR',
                      'FOB_FC', 'FOB_USD', 'EXCHANGE_RATE', 'IMPORTER_NAME', 'IMPORTER_ADDRESS', 'COUNTRY_OF_ORIGIN',
                      'PORT_OF_LOADING', 'PORT_OF_DISCHARGE', 'PORT_CODE', 'MODE_OF_PORT', 'EXPORTER_ID',
                      'EXPORTER_NAME', 'EXPORTER_ADDRESS', 'EXPORTER_CITY', 'EXPORTER_PIN']

            workbook = xlwt.Workbook()
            xlsx_sheet = workbook.add_sheet('shipments_data')
            xlsx_sheet = self.write_header(xlsx_sheet, header)
            data = list()
            qs = self.get_queryset().order_by('SB_DATE')[:excel_limit]

            for index, user_obj in enumerate(qs):
                temp_data_row = list()
                temp_data_row.append(str(index + 1))
                temp_data_row.append('EXPORTER')
                for index, field in enumerate(fields):
                    if field == 'SB_DATE' and user_obj.SB_DATE:
                        date = user_obj.SB_DATE.strftime("%d-%m-%Y")
                        temp_data_row.append(date)
                    elif field == 'COUNTRY' and user_obj.COUNTRY:
                        temp_data_row.append(user_obj.COUNTRY.name)
                    elif hasattr(user_obj, field):
                        if getattr(user_obj, field) is not None:
                            temp_data_row.append(str(getattr(user_obj, field)))
                        else:
                            temp_data_row.append('')
                    else:
                        temp_data_row.append('')
                    if len(fields) == index + 1:
                        data.append(temp_data_row)
            for row_index, value in enumerate(data):
                for col_index, field_value in enumerate(value):
                    xlsx_sheet.write(row_index + 1, col_index, field_value)
            workbook.save(response)
            return response
        else:
            response = HttpResponse(content_type='application/ms-excel')
            filename = "Importers_" + "shipments" + "_" + str(uuid.uuid4())[-4:] + ".xls"

            response['Content-Disposition'] = f'attachment; filename={filename}'
            header = ['S.No', 'TYPE', 'COUNTRY', 'DATE', 'MONTH', 'YEAR', 'HS CODE', 'TWO DIGIT', 'FOUR DIGIT',
                      'HS CODE DESCRIPTION', 'UNIT', 'QUANTITY', 'CURRENCY', 'UNT PRICE_FC', 'INV VALUE_FC',
                      'UNT PRICE INR', 'INVOICE NUMBER', 'BE NUMBER', 'UNIT RATE WITH DUTY', 'PER UNT DUTY', 'DUTY INR',
                      'DUTY FC', 'DUTY PERCENT', 'EX TOTAL VALUE', 'ASS VALUE INR', 'ASS VALUE USD', 'ASS VALUE FC',
                      'EXCHANGE RATE', 'EXPORTER NAME', 'EXPORTER ADDRESS',
                      'COUNTRY OF ORIGIN', 'PORT OF LOADING', 'PORT OF DISCHARGE', 'PORT CODE',
                      'MODE OF PORT', 'IEC', 'IMPORTER NAME', 'IMPORTER ADDRESS', 'IMPORTER CITY AND STATE',
                      'IMPORTER_PIN', 'IMPORTER PHONE', 'IMPORTER EMAIL', 'IMPORTER CONTACT PERSON', 'BE TYPE',
                      'CHA NAME', 'Item No']

            fields = ['COUNTRY', 'BE_DATE', 'MONTH', 'YEAR', 'RITC', 'TWO_DIGIT', 'FOUR_DIGIT', 'RITC_DISCRIPTION',
                      'UQC', 'QUANTITY', 'CURRENCY', 'UNT_PRICE_FC', 'INV_VALUE_FC',
                      'UNT_PRICE_INR', 'INV_NO', 'BE_NO', 'UNT_RATE_WITH_DUTY', 'PER_UNT_DUTY', 'DUTY_INR', 'DUTY_FC',
                      'DUTY_PERCENT', 'EX_TOTAL_VALUE', 'ASS_VALUE_INR', 'ASS_VALUE_USD', 'ASS_VALUE_FC',
                      'EXCHANGE_RATE', 'EXPORTER_NAME', 'EXPORTER_ADDRESS', 'COUNTRY_OF_ORIGIN',
                      'PORT_OF_LOADING', 'PORT_OF_DISCHARGE', 'PORT_CODE', 'MODE_OF_PORT', 'IMPORTER_ID',
                      'IMPORTER_NAME', 'IMPORTER_ADDRESS', 'IMPORTER_CITY_STATE', 'IMPORTER_PIN', 'IMPORTER_PHONE',
                      'IMPORTER_EMAIL', 'IMPORTER_CONTACT_PERSON', 'BE_TYPE', 'CHA_NAME', 'Item_No']

            workbook = xlwt.Workbook()
            xlsx_sheet = workbook.add_sheet('shipments_data')
            xlsx_sheet = self.write_header(xlsx_sheet, header)
            data = list()
            qs = self.get_queryset().order_by('BE_DATE')[:excel_limit]

            for index, user_obj in enumerate(qs):
                temp_data_row = list()
                temp_data_row.append(str(index + 1))
                temp_data_row.append('IMPORTER')
                for index, field in enumerate(fields):
                    if field == 'BE_DATE' and user_obj.BE_DATE:
                        date = user_obj.BE_DATE.strftime("%d-%m-%Y")
                        temp_data_row.append(date)
                    elif field == 'COUNTRY' and user_obj.COUNTRY:
                        temp_data_row.append(user_obj.COUNTRY.name)
                    elif hasattr(user_obj, field):
                        if getattr(user_obj, field) is not None:
                            temp_data_row.append(str(getattr(user_obj, field)))
                        else:
                            temp_data_row.append('')
                    else:
                        temp_data_row.append('')
                    if len(fields) == index + 1:
                        data.append(temp_data_row)
            for row_index, value in enumerate(data):
                for col_index, field_value in enumerate(value):
                    xlsx_sheet.write(row_index + 1, col_index, field_value)
            workbook.save(response)
            return response


class ExporterImporterList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (djfilters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,
                       )
    search_fields = None

    def get_serializer_class(self):
        data_type = self.request.query_params.get("data_type")
        if data_type == "export":
            return ImporterNameSerializer
        else:
            return ExporterNameSerializer

    def get_queryset(self):
        data_type = self.request.query_params.get("data_type")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        country = self.request.query_params.get("country")
        if data_type == "export":
            model = ExportTable
            self.search_fields = ('IMPORTER_NAME',)
            queryset = model.objects.filter(COUNTRY__id=country, SB_DATE__date__gte=start_date,
                                            SB_DATE__date__lte=end_date).distinct('IMPORTER_NAME')
        else:
            model = ImportTable
            self.search_fields = ('EXPORTER_NAME',)
            queryset = model.objects.filter(COUNTRY__id=country, BE_DATE__date__gte=start_date,
                                            BE_DATE__date__lte=end_date).distinct('EXPORTER_NAME')
        return queryset










