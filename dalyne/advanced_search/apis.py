from django.db.models import Q
from rest_framework import generics, permissions
from core_module.models import ImportTable, ExportTable, Plans, \
    ProductMaster, CompanyMaster, CountryMaster, FilterDataModel
from import_export.serializers import ImporterDataFilterSerializer, ExporterDataFilterSerializer


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
                return qs
            else:
                return {}
        else:
            return {}
