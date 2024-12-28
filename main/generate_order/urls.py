from django.urls import path
from . import views

urlpatterns = [
    path('generate_order/', views.trade_form, name='trade_form'),
]
