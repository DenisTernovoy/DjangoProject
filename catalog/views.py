from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Product, Contacts, Category
from django.core.paginator import Paginator


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
    paginator = Paginator(products, 6)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    return render(request, "home.html", context={"page_obj": page_obj})


def show_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "show_product.html", context=context)


def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("textarea")
        price = request.POST.get("price")
        category = request.POST.get("category")

        if "file" in request.FILES:
            photo = request.FILES["file"]
        else:
            photo = None

        existing = list(
            map(lambda x: x.lower(), Product.objects.values_list("name", flat=True))
        )

        if name.lower() in existing:
            categories = Category.objects.all()
            context = {"categories": categories, "existing": True}
            print("OK")
            return render(request, "add_product.html", context=context)
        else:
            categories = Category.objects.all()
            context = {"categories": categories, "existing": False}
            category = Category.objects.get(name=category)
            new_product = Product(
                name=name,
                description=description,
                price=price,
                category=category,
                image=photo,
            )
            new_product.save()
            return render(request, "add_product.html", context=context)

    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "add_product.html", context=context)
