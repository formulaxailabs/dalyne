from django.urls import path
from django.conf.urls import url, include
from import_export import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('workspace', views.WorkSpaceAPI, basename="workspace")

app_name = 'import_export'


urlpatterns = [
    url(r'^', include(router.urls)),
    path('excel/data/upload/', views.ExcelDataImportView.as_view(), name='excel-import'),
    path('plans/list/', views.PlansListView.as_view(), name='plans'),
    path('products/list/', views.ProductListAPI.as_view(), name='product-filter-list'),
    path('company/list/', views.CompanyListAPI.as_view(), name='company-filter-list'),
    path('products/file/upload/', views.ProductDataImportAPI.as_view(), name='product-import'),
    path('companies/file/upload/', views.CompanyDataImportAPI.as_view(), name='company-import'),
    path('countries/list/', views.CountriesListAPI.as_view(), name='countries'),
    path('advanced/search/data/', views.AdvancedSearchAPI.as_view(), name='advanced-search'),
    path('filtered/data/', views.FilterDataGetAPI.as_view(), name='filter-data'),
    path('delete/duplicate/companies/', views.DeleteDuplicateCompaniesAPI.as_view(), name='duplicate-delete')

]