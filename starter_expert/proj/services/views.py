import io
import xlsxwriter
from . import utils
from .forms import Upload_nmids_form
from . import tasks
from django.http import FileResponse
from .models import IndexerReports, IndexerReportsData
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
    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = Upload_nmids_form(request.POST, request.FILES)
        if form.is_valid():
            file_operator = utils.FileOperator()
            nmids = file_operator.iterate_nmids(request.FILES['file'].file)
            for nmid in nmids:
                report = IndexerReports.objects.create(nmid=nmid, user=user)
                tasks.create_report_data.delay(nmid=report.nmid, report_id=report.id)
    else:
        form = Upload_nmids_form()

    reports = IndexerReports.objects.filter(user=user)
    paginator = Paginator(reports, 25)
    page_number = request.GET.get('page')
    page_content = paginator.get_page(page_number)
    return render(request, 'services/indexer.html', {'form': form, 'page_content': page_content})


# вьюха для скачивания файла по определенному отчету
@login_required(login_url='login')
def download_report(request, report_id):
    # запрос с бд, чтобы узнать nmid по этому report_id
    report = IndexerReports.objects.get(id=report_id)
    report_nmid = report.nmid
    # создание файлового оператор и получение объекта buffer
    # внутри которого уже создан отчет в .xlsx файле
    fileOperator = utils.FileOperator()
    buffer = fileOperator.create_report_buffer(report_id)

    return FileResponse(buffer, as_attachment=True, filename=f'{report_nmid}.xlsx')