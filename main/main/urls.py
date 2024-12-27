from django.contrib import admin
from django.urls import path
from .views import home, generate_order, current_progress

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('generate_order/', generate_order, name='generate_order'),
    path('current_progress/', current_progress, name='current_progress'),
]
