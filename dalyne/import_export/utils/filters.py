from django_filters import rest_framework as filters_rest
from core_module.models import ProductMaster


class ProductFilter(filters_rest.FilterSet):
    hs_code = filters_rest.CharFilter(method="filter_hs_code")
    digits = filters_rest.CharFilter(method="filter_digits")

    class Meta:
        model = ProductMaster
        fields = ['id']

    def filter_hs_code(self, queryset, name, hs_code):
        if hs_code:
            return queryset.filter(hs_code__istartswith=hs_code)
        else:
            return queryset

    def filter_digits(self, queryset, name, digits):
        if digits:
            return queryset.filter(digits=digits)
        else:
            return queryset
