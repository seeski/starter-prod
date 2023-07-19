from .utils import Indexer
from celery import shared_task
from .models import IndexerReportsData, IndexerReports


@shared_task
def create_report_data(nmid, report_id):
    report = IndexerReports.objects.filter(id=report_id)[0]
    indexer = Indexer(nmid)
    for data in indexer.iterate_queries():
        priority_cat = data.get('top_category')
        keywords = data.get('keyword')
        frequency = data.get('frequency')
        req_depth = data.get('req_depth')
        existence = data.get('existence')
        place = data.get("place")
        spot_req_depth = data.get('spot_req_depth')
        ad_spots = data.get('ad_spots')
        ad_place = data.get('ad_place')


        data_obj = IndexerReportsData.objects.create(
            nmid=nmid,
            priority_cat=priority_cat,
            keywords=keywords,
            frequency=frequency,
            req_depth=req_depth,
            existence=existence,
            place=place,
            spot_req_depth=spot_req_depth,
            ad_place=ad_place,
            ad_spots=ad_spots,
            report_id=report,
        )
    report = IndexerReports.objects.get(id=report_id)
    report.ready = True
    report.save()