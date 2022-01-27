import os
from io import StringIO, BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from core.utils import generate_figure

def home(request):
    context = {}
    if request.method == "POST":
        if 'btnGenGraph' in request.POST:
            context = generate_graph(request)
        elif 'btnDlImage' in request.POST:
            return download_graph(request)
        else:
            print("Download Data")
    return render(request, 'home.html', context)


def generate_graph(request):
    serie1 = request.POST.get('serie1', '')
    serie2 = request.POST.get('serie2', '')
    serie3 = request.POST.get('serie3', '')
    serie4 = request.POST.get('serie4', '')
    start = request.POST.get('datepicker1')
    end = request.POST.get('datepicker2')

    fig = generate_figure(serie1, serie2, serie3, serie4, "{}/{}".format(start, end))
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    graph = imgdata.getvalue()
    context = {
        "serie1": serie1,
        "serie2": serie2,
        "serie3": serie3,
        "serie4": serie4,
        "datepicker1": start,
        "datepicker2": end,
        "graph": graph
    }
    return context


def download_graph(request):
    if request.method == "POST":
        serie1 = request.POST.get('serie1', '')
        serie2 = request.POST.get('serie2', '')
        serie3 = request.POST.get('serie3', '')
        serie4 = request.POST.get('serie4', '')
        start = request.POST.get('datepicker1')
        end = request.POST.get('datepicker2')

        fig = generate_figure(serie1, serie2, serie3, serie4, "{}/{}".format(start, end))
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)

        response = HttpResponse(imgdata, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=vizapp.png'
        return response


def download_excel(request):
    path = os.path.join(settings.STATIC_ROOT, 'Nombres Series Easyviz.xlsx')
    if os.path.exists(path):
        with open(path, 'rb') as excel:
            data = excel.read()
        response = HttpResponse(data, content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename=Nombres Series Easyviz.xlsx'
        return response
    return render(request, 'home.html', {})
