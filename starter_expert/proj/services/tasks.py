import datetime

from .utils import Indexer
from celery import shared_task
from . import utils
from .models import (
    IndexerReportData, IndexerReport, NmidToBeReported,
    SeoReport, SeoReportData
)
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.utils import IntegrityError


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
def seo_collector(query, depth, user_id):
    """Запускает SeoCollector"""
    try:
        collector = utils.SeoCollector(query, depth, user_id)
        collector.run()
    # Если запись в базе данных будет удалена,
    # то роняется эта ошибка. Мы её и обраба-
    # тываем
    except IntegrityError:
        pass


'''
@shared_task
def delete_old_seo_collectors():
    """Удаляет висячие запросы из SeoCollectora (которые были не до конца завершены),
    и удаляет запросы хранящиеся в базе данных целый месяц"""
    now = datetime.datetime.now()
    month = datetime.timedelta(weeks = 4)
    six_hour = datetime.timedelta(hours = 6)

    # Выделяем в базе queries, которые уже лежат месяц (неактуальные) и
    # по которым до конца небыло собрано достаточно информации
    queries = SeoReport.objects.filter(
        (Q(create_date__lt=now - month)) | \
        (Q(completed=False) & Q(create_date__lt = now - six_hour))
    ).delete()


@shared_task
def update_seo_collectors():
    now = datetime.datetime.now()
    day = datetime.timedelta(days=1)
    queries = SeoReport.objects.prefetch_related("keywords").all()

    for query in queries:
        query.keywords.all().delete()
        tasks.seo_collector(query)
'''