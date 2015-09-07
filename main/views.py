from django.shortcuts import render
from .models import MainData


def index(request):
    return render(request, 'main/index.html',
                  {'result': MainData.objects.all()})
