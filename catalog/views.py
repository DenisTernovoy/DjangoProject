from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product, Contacts


# Create your views here.


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Мы обязательно Вам перезвоним.")

    return render(request, "contacts.html", {"country_data": Contacts.objects.all()[0]})


def home(request):
    products = Product.objects.all()[:5]
    for product in products:
        print(product)
    return render(request, "home.html")
