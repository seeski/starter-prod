from django.contrib import admin
from .models import (
	IndexerReport, IndexerReportData, NmidToBeReported,
	QuerySeoCollector,KeywordsSeoCollector
)
# Register your models here.

admin.site.register(IndexerReport)
admin.site.register(IndexerReportData)
admin.site.register(NmidToBeReported)

### SEO COLLECTOR ###
admin.site.register(QuerySeoCollector)
admin.site.register(KeywordsSeoCollector)
#####################