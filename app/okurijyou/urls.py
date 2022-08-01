from django.urls import path
from .views import create_csv

urlpatterns =[
    path('', create_csv, name='okurijyou')
]