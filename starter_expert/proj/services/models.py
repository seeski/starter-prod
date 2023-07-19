from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# хранит данные об отчетах
# поле nmid хранит данные о том, какой id товара нужно проиндексировать
# поле date хранит дату создания отчета
# поле ready показывает, созданы ли и укомплектованы ли данные по отчету в модели IndexerReportsData
# поле user показывает какой пользователь подгрузил определнный nmid на создание отчета
# для каждого пользователя доступны только созданные им отчеты
class IndexerReports(models.Model):

    nmid = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True)
    ready = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


#  хранит собранные данные по каждому отчету
#  nmid - хранит в себе id товара, который был проиндексирован. Возможно поле в последующем удалиться за ненадобностью
#  priority_cat - хранит данные о приоритетной категории по определенному запросу
# keywords - хранится строка с поисковым запросом, по которому было совпадение
# frequency - лежит число запросов за x времени из файлика requests.csv (насколько популярен запрос)
# rep_depth - хранится дата о кол-ве выданных результатов по определенному запросу
# existence - есть ли товар в поисковой выдаче по данному запросу
# place - место в поисковой выдаче в пределах 1000 запросов (за пределами 1000 место не определяется)
#  spot_req_depth - процент топа поисковой выдачи (если место товара в пределах первой 1000)
# ad_spots - кол-во рекламных мест
# ad_place - место в рекламной выдаче
# report_id - внешний ключ связывающий отчет с записью в
class IndexerReportsData(models.Model):

    nmid = models.IntegerField(null=False)
    priority_cat = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    frequency = models.IntegerField()
    req_depth = models.IntegerField()
    existence = models.BooleanField()
    place = models.IntegerField(null=True, default=None)
    spot_req_depth = models.CharField(null=True, default=None, max_length=255)
    ad_spots = models.IntegerField(null=True, default=None)
    ad_place = models.IntegerField(null=True, default=None)
    report_id = models.ForeignKey(IndexerReports, null=False, on_delete=models.CASCADE)
