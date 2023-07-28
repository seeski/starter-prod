import io
import xlsxwriter
import datetime

from . import utils
from .forms import Upload_nmids_form, QueryForm
from .models import (
    IndexerReportData, IndexerReport, NmidToBeReported,
    QuerySeoCollector, KeywordsSeoCollector
)
from . import tasks
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404

# лк со всеми инструментами
@login_required(login_url='login')
def cabinet(request):
    return render(request, 'services/cabinet.html', {})

# страница с индексатором
@login_required(login_url='login')
def indexer(request):
    # user = User.objects.get(id=user_id)
    # user_id = request.user_id
    user = request.user
    user_id = user.id


    if request.method == 'POST':
        form = Upload_nmids_form(request.POST, request.FILES)
        if form.is_valid():
            fileOperator = utils.FileOperator()
            nmids = fileOperator.iterate_nmids(request.FILES['file'].file)
            for nmid in nmids:
                tasks.createNmidToReport.delay(nmid, user_id)

    else:
        form = Upload_nmids_form()

    nmids = NmidToBeReported.objects.filter(user=user)
    paginator = Paginator(nmids, 25)
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    return render(request, 'services/indexer.html', {'form': form, 'page_content': page_content})

# @login_required(login_url='login')
# def indexer(request):
#     user_id = request.user.id
#     user = User.objects.get(id=user_id)
#
#
#     if request.method == 'POST':
#         form = Upload_nmids_form(request.POST, request.FILES)
#         if form.is_valid():
#             file_operator = utils.FileOperator()
#             nmids = file_operator.iterate_nmids(request.FILES['file'].file)
#             for nmid in nmids:
#                 try:
#                     models.NmidsToBeReported.objects.create(
#                         nmid=nmid,
#                         user=user
#                     )
#                 except Exception as e:
#                     print(f'some exc{e}')
#                     continue
#     else:
#         form = Upload_nmids_form()
#
#
#     nmids = models.NmidsToBeReported.objects.order_by('date')
#     paginator = Paginator(nmids, 30)
#     page_number = request.GET.get('page')
#     page_content = paginator.get_page(page_number)
#     return render(request, 'services/indexer.html', {'page_content': page_content})


# страница с отчетами по индексатору
@login_required(login_url='login')
def indexerReports(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    reports = IndexerReport.objects.filter(user=user).order_by('date')
    paginator = Paginator(reports, 25)
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    return render(request, 'services/indexerReports.html', {'page_content': page_content})


# вьюха для скачивания файла по определенному отчету
@login_required(login_url='login')
def download_report(request, report_id):
    # запрос с бд, чтобы узнать nmid по этому report_id
    report = IndexerReport.objects.get(id=report_id)
    report_nmid = report.nmid
    # создание файлового оператор и получение объекта buffer
    # внутри которого уже создан отчет в .xlsx файле
    fileOperator = utils.FileOperator()
    buffer = fileOperator.create_report_buffer(report_id)

    return FileResponse(buffer, as_attachment=True, filename=f'{report_nmid}.xlsx')


def detailReportInfo(request, reports_nmid):
    reports = IndexerReport.objects.filter(user=request.user, nmid=reports_nmid).order_by('date')
    paginator = Paginator(reports, 25)
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    return render(request, 'services/indexerReports.html', {'page_content': page_content})


@login_required(login_url='login')
def download_seo_collector_query(request):
    pk = request.GET.get('pk')
    fileOperator = utils.FileOperator()

    if pk.isdigit():
        pk = int(pk)
        query_obj = QuerySeoCollector.objects.prefetch_related("keywords").filter(pk=pk).first()
        query = query_obj.query
        depth = query_obj.depth
        if query_obj is not None:
            if query_obj.completed:
                buffer = fileOperator.create_seo_collector_buffer(query_obj)

                return FileResponse(buffer, as_attachment=True, filename=f'{query} {depth}.xlsx')

    raise Http404


@login_required(login_url='login')
def seo_collector_all_query(request):
    """Страница запросов по seo wildberries"""
    if request.POST:
        form = QueryForm(request.POST)
        if form.is_valid():
            tasks.seo_collector.delay(form.cleaned_data['query'], form.cleaned_data['depth'])
            return redirect(seo_collector_all_query)
    else:
        paginator = Paginator(QuerySeoCollector.objects.all(), 25)
        page_number = request.GET.get('page')
        page_content = paginator.get_page(page_number)
        return render(
            request,
            'services/seo_collector_all_query.html',
            {
                'page_content': page_content
            }
        )


@login_required(login_url='login')
def seo_collector_query(request):
    """Подробная страница query. seo для wildberries"""
    pk = request.GET.get('pk')

    if pk is None:
        return redirect(seo_collector_all_query)
    if not pk.isdigit():
        raise Http404

    query_obj = QuerySeoCollector.objects\
                    .prefetch_related("keywords")\
                    .filter(pk=pk)\
                    .first()

    paginator = Paginator(query_obj.keywords.all(), 25)
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)

    return render(
        request, 
        'services/seo_collector_query.html', 
        {
            'page_content': page_content, 
            'paginator': paginator,
            'pk': pk,
        }
    )
