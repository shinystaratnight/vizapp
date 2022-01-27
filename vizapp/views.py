import os
from io import StringIO, BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from core.utils import generate_figure, generate_data
from vizapp.forms import VizForm
import pandas as pd
import seaborn as sns


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
            periodo = form.get_periodo()
            color_fondo = form.cleaned_data.get("color_fondo")
            Marcar_recesiones = form.cleaned_data.get("Marcar_recesiones")
            Linea_cero = form.cleaned_data.get("Linea_cero")

            Eje_secundario2 = form.cleaned_data.get("Eje_secundario2")
            Eje_secundario3 = form.cleaned_data.get("Eje_secundario3")
            Eje_secundario4 = form.cleaned_data.get("Eje_secundario4")

            color_linea1 = form.cleaned_data.get("color_linea1")
            color_linea2 = form.cleaned_data.get("color_linea2")
            color_linea3 = form.cleaned_data.get("color_linea3")
            color_linea4 = form.cleaned_data.get("color_linea4")

            Tipo1 = form.cleaned_data.get("Tipo1")
            Tipo2 = form.cleaned_data.get("Tipo2")
            Tipo3 = form.cleaned_data.get("Tipo3")
            Tipo4 = form.cleaned_data.get("Tipo4")

            if 'btnGenGraph' in request.POST:
                context['graph'] = generate_graph(
                    request, serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                          Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4,
                          Tipo1, Tipo2, Tipo3, Tipo4)
            elif 'btnDlImage' in request.POST:
                return download_graph(
                    request, serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                          Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4,
                          Tipo1, Tipo2, Tipo3, Tipo4)
            else:
                return download_data(
                    request, serie1, serie2, serie3, serie4, periodo)
    else:
        form = VizForm()
    context['form'] = form
    return render(request, 'home.html', context)


def generate_graph(request, serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                    Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4, Tipo1, Tipo2, Tipo3, Tipo4):
    sns.set_style('darkgrid')
    fig = generate_figure(serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                          Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4, Tipo1, Tipo2, Tipo3, Tipo4)
    imgData = StringIO()
    fig.savefig(imgData, format='svg', bbox_inches="tight")
    imgData.seek(0)
    graph = imgData.getvalue()
    return graph


def download_graph(request, serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                   Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4, Tipo1, Tipo2, Tipo3, Tipo4):
    sns.set_style('darkgrid')
    fig = generate_figure(serie1, serie2, serie3, serie4, periodo, color_fondo, Marcar_recesiones, Linea_cero,
                          Eje_secundario2, Eje_secundario3, Eje_secundario4,
                          color_linea1, color_linea2, color_linea3, color_linea4, Tipo1, Tipo2, Tipo3, Tipo4)
    imgData = BytesIO()
    fig.savefig(imgData, format='png', bbox_inches="tight")
    imgData.seek(0)

    response = HttpResponse(imgData, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename=vizapp.png'
    return response


def download_data(request, serie1, serie2, serie3, serie4, periodo):
    df = generate_data(serie1, serie2, serie3, serie4, periodo)
    excel_file = BytesIO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(xlwriter, 'Sheet1')
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)

    response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data.xlsx'
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

