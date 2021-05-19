from django.urls import path, include
from django.conf.urls import url
from import_export import views

app_name = 'import_export'


urlpatterns = [
    path('excel-data-import/', views.ExcelDataImportView.as_view(), name='excel-import'),
    path('plans/list/', views.PlansListView.as_view(), name='plans'),
    path('import-export-list/', views.ImportExportListView.as_view(), name='import-export'),
    path('product-filter-list/', views.ProductFilterListView.as_view(), name='product-filter-list'),
    path('company-filter-list/', views.CompanyFilterListView.as_view(), name='company-filter-list'),
    path('products/file/upload/', views.ProductDataImportAPI.as_view(), name='product-import'),
    path('companies/file/upload/', views.CompanyDataImportAPI.as_view(), name='company-import')

]