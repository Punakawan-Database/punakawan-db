from django.shortcuts import render

# Create your views here.
def diskon(request):
    return render(request, 'diskon.html')