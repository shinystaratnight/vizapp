from django.shortcuts import render
from django.http import HttpResponse
from core.utils import get_nombres_series

def home(request):
    nombres_series = get_nombres_series()
    return HttpResponse('Hello')
