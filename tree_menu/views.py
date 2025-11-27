from django.shortcuts import render
def home(request):
    return render(request, "home.html")
def page(request, slug):
    return render(request, "page.html", {"slug": slug})
