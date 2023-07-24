from django.contrib import admin
from .models import IndexerReport, IndexerReportData, NmidToBeReported
# Register your models here.

admin.site.register(IndexerReport)
admin.site.register(IndexerReportData)
admin.site.register(NmidToBeReported)