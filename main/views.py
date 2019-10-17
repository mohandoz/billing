from django.shortcuts import render


def home(request):
    template_name = "main/home.html"
    if request.method == "GET":
        return render(request, template_name)
