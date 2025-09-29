from django.shortcuts import render, get_object_or_404
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
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "home.html", context=context)


def show_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "show_product.html", context=context)
