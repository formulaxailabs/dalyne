from django.urls import path, include
from django.conf.urls import url
from import_export import views

app_name = 'import_export'


urlpatterns = [
    path('excel-data-import/', views.ExcelDataImportView.as_view(), name='excel-import'),
    path('plans-listView/', views.PlansListView.as_view(), name='plans'),
    path('import-export-list/', views.ImportExportListView.as_view(), name='import-export'),
    
]