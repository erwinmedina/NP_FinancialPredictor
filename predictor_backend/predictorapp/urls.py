from django.urls import path
from . import views

urlpatterns = [
    path('financial-records/', views.get_financial_records, name='get_financial_records'),
    path('add-financial-record/', views.add_financial_record, name='add_financial_record'),
]
