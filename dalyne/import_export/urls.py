from django.urls import path, include
from django.conf.urls import url
from import_export import views

app_name = 'import_export'


urlpatterns = [
    path('excel/data/upload/', views.ExcelDataImportView.as_view(), name='excel-import'),
    path('plans/list/', views.PlansListView.as_view(), name='plans'),
    path('products/list/', views.ProductListAPI.as_view(), name='product-filter-list'),
    path('company/list/', views.CompanyListAPI.as_view(), name='company-filter-list'),
    path('products/file/upload/', views.ProductDataImportAPI.as_view(), name='product-import'),
    path('companies/file/upload/', views.CompanyDataImportAPI.as_view(), name='company-import'),
    path('countries/list/', views.CountriesListAPI.as_view(), name='countries'),
    path('advanced/search/data/', views.AdvancedSearchAPI.as_view(), name='advanced-search')

]