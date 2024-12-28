from django.urls import path
from . import views

urlpatterns = [
    path('generate_order/', views.trade_form, name='trade_form'),
    path('current_progress/', views.current_progress, name='current_progress'),
]
