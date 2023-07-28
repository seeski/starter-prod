import datetime

from .utils import Indexer
from celery import shared_task
from . import utils
from .models import (
    IndexerReportData, IndexerReport, NmidToBeReported,
    QuerySeoCollector, KeywordsSeoCollector
)
from django.contrib.auth.models import User


# таска для создание записи о определенном nmid
# таска потому что обращаемся к апи вб
# если nmid в подгружаемом файле будет много, то клиент будет долго ждать ответа
@shared_task
def createNmidToReport(nmid, user_id):
    nmid_url = f'https://www.wildberries.ru/catalog/{nmid}/detail.aspx'
    user = User.objects.get(id=user_id)
    urlOperator = utils.URLOperator()
    dataCollector = utils.DataCollector()

    detail_url = urlOperator.create_nmid_detail_url(nmid)
    name = dataCollector.get_brand_and_name(detail_url)
    # создание записи в модели обернул в try/except из-за значения unique=True
    # если клиент случайно подгрузит уже существующий в таблице nmid, то поднимется ошибка
    try:
        NmidToBeReported.objects.create(
            nmid=nmid,
            name=name,
            url=nmid_url,
            user=user
        )

    except Exception as e:
        print(e)
        print("HI")


@shared_task
def iterateNmids():
    queries = NmidToBeReported.objects.all()
    for query in queries:
        report = IndexerReport.objects.create(
            nmid=query.nmid,
            user=query.user
        )
        utils.createReportData(report)

    reports = IndexerReport.objects.filter(ready=False)

    for report in reports:
        utils.createReportData(report)
        

@shared_task
def seo_collector(query, depth):
    """Запускает SeoCollector"""
    collector = utils.SeoCollector(query, depth)
    collector.run()


@shared_task
def clear_old_seo_collectors():
    """Удаляет висячие запросы из SeoCollectora (которые были не до конца завершены),
    и удаляет запросы хранящиеся в базе данных целый месяц"""
    queries = QuerySeoCollector.objects.all()

    for query in queries:
        if query.create_date < (datetime.now() - datetime.timedelta(month = 1)):
            query.delete()

        if query.create_date < (datetime.now() - datetime.timedelta(day = 1)) and not query.completed:
            query.delete()

