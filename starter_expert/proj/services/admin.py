from django.contrib import admin
from .models import (
	IndexerReport, IndexerReportData, NmidToBeReported,
	SeoReport,SeoReportData
)
# Register your models here.

admin.site.register(IndexerReport)
admin.site.register(IndexerReportData)
admin.site.register(NmidToBeReported)

### SEO COLLECTOR ###
admin.site.register(SeoReport)
admin.site.register(SeoReportData)
#####################