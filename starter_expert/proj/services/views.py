import io
import xlsxwriter
from . import utils
from .forms import Upload_nmids_form
from .models import IndexerReportData, IndexerReport, NmidToBeReported
from . import tasks
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.

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