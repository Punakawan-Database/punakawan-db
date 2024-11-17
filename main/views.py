from django.shortcuts import render

def show_main(request):
    context = {
        'name' : 'Stranger'
    }

    return render(request, "main.html", context)
