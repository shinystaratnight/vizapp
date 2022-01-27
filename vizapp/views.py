import os
from io import StringIO, BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from core.utils import generate_figure
from vizapp.forms import VizForm


def home(request):
    context = {}
    if request.method == "POST":
        if 'btnDlExcel' in request.POST:
            return download_excel(request)

        form = VizForm(request.POST)
        if form.is_valid():
            serie1 = form.cleaned_data.get('serie1')
            serie2 = form.cleaned_data.get('serie2')
            serie3 = form.cleaned_data.get('serie3')
            serie4 = form.cleaned_data.get('serie4')
            fechas = form.fechas()

            if 'btnGenGraph' in request.POST:
                context['graph'] = \
                    generate_graph(request, serie1, serie2, serie3, serie4, fechas)
            elif 'btnDlImage' in request.POST:
                return download_graph(request, serie1, serie2, serie3, serie4, fechas)
            else:
                print("Download Data")
    else:
        form = VizForm()
    context['form'] = form
    return render(request, 'home.html', context)


def generate_graph(request, serie1, serie2, serie3, serie4, fechas):
    fig = generate_figure(serie1, serie2, serie3, serie4, fechas)
    imgData = StringIO()
    fig.savefig(imgData, format='svg')
    imgData.seek(0)
    graph = imgData.getvalue()
    return graph


def download_graph(request, serie1, serie2, serie3,serie4, fechas):
    fig = generate_figure(serie1, serie2, serie3, serie4, fechas)
    imgData = BytesIO()
    fig.savefig(imgData, format='png')
    imgData.seek(0)

    response = HttpResponse(imgData, content_type='image/png')
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
