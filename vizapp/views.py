from io import StringIO, BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from core.utils import generate_figure

def home(request):
    context = {}
    if request.method == "POST":
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
        context["graph"] = graph
        context = {
            "serie1": serie1,
            "serie2": serie2,
            "serie3": serie3,
            "serie4": serie4,
            "datepicker1": start,
            "datepicker2": end,
            "graph": graph
        }

    return render(request, 'home.html', context)

def download(request):
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

