from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def generate_order(request):
    # Logic for generating a new order
    return render(request, 'generate_order.html')

def current_progress(request):
    # Logic for showing current progress
    return render(request, 'current_progress.html')
