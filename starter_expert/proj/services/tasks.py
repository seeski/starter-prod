from .utils import Indexer
from celery import shared_task
from . import utils
from .models import IndexerReportData, IndexerReport, NmidToBeReported
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


#
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