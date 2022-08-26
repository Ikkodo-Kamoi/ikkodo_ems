# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def example(request):
    return render(request, 'analytics/dashbord.html')