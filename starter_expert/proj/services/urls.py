from django.urls import path
from . import views

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('indexer/', views.indexer, name='indexer'),
    path('indexer/reports/', views.indexerReports, name='indexerReports'),
    path('indexer/reports/<int:reports_nmid>', views.detailReportInfo, name='detail-report-info'),
    path('download/<int:report_id>/', views.download_report, name='download_report'),
    path('seocollector/all-query/', views.seo_collector_all_query, name='seo_collector_all_query'),
    path('seocollector/query/', views.seo_collector_query, name='seo_collector_query'),
    path('seocollector/download-seo-collector-query/', views.download_seo_collector_query, name='download_seo_collector_query'),
    path('seocollector/delete/<int:query_pk>/', views.delete_seo_report, name='delete_seo_report'),
    path('seocollector/query/checked_box/', views.add_reference_seo_report_data, name='add_reference_seo_report_data')
]