from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {
        'page_theme': 'dark',
    })


def fvsa(request):
    return render(request, 'fvsa.html', {
        'page_theme': 'light',
    })