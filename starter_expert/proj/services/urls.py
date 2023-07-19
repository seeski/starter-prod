from django.urls import path
from . import views

urlpatterns = [
    path('cabinet/', views.cabinet, name='cabinet'),
    path('indexing/', views.indexer, name='indexer'),
    path('download/<int:report_id>/', views.download_report, name='download_report'),
]