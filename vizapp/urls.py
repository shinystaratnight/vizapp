from django.urls import path
from . import views

app_name = "vizapp"

urlpatterns = [
    path('', views.home, name="home"),
    path('/download-graph', views.download_graph, name="download-graph"),
    path('/download-excel', views.download_excel, name="download-excel")
]
