from .utils import Indexer
from celery import shared_task
from .models import IndexerReportsData, IndexerReports

# эта таска собирает и записывает данные для определенного отчета из модели IndexerReports
@shared_task
def create_report_data(nmid, report_id):

    # объект моделри IndexerReports, а не просто report_id, нужен
    # чтобы передать его в качестве внешнего ключа в поле report_id модели IndexerReportsData
    report = IndexerReports.objects.filter(id=report_id)[0]
    indexer = Indexer(nmid)

    # здесь просто пробегаемся по методу-итератору класса Indexer
    # подробнее можно глянуть в utils
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

        # создаем новую запись в модели из данных полученных генератором
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

    # после того, как луп закончил свою работу, меняем флажок ready на значение True
    # поле ready хранит значение о готовности отчета
    # если значение True, то данные по отчету готовы и его можно скачивать
    report = IndexerReports.objects.get(id=report_id)
    report.ready = True
    report.save()