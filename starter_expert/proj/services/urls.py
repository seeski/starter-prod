from django.urls import path
from . import views

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('indexer/', views.indexer, name='indexer'),
    path('indexer/reports/', views.indexerReports, name='indexerReports'),
    path('indexer/reports/<int:reports_nmid>', views.detailReportInfo, name='detail-report-info'),
    path('download/<int:report_id>/', views.download_report, name='download_report'),
]