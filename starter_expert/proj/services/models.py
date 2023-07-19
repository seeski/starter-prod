from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IndexerReports(models.Model):

    nmid = models.IntegerField(null=False)
    date = models.DateField(auto_now_add=True)
    ready = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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


class ToTest(models.Model):
    nmid = models.IntegerField()

    def __str__(self):
        return f'congratulations {self.nmid}'