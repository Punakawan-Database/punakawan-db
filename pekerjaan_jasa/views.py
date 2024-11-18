from django.shortcuts import render


def pekerjaan_jasa(request):
    return render(request, "pekerjaan_jasa.html")


def pekerjaan_jasa_status(request):
    return render(request, "pekerjaan_jasa_status.html")
