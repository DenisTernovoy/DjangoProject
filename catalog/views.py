from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy

from catalog.models import Product, Contacts, Category
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.


class ProductListView(ListView):
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = Paginator(Product.objects.all(), 6)
        page_num = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_num)

        context["page_obj"] = page_obj

        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "description", "price", "category", "image"]
    success_url = reverse_lazy("catalog:product_list")


class ContactsView(View):
    model = Contacts
    template_name = "catalog/contacts_view.html"

    def get(self, request):
        context = {"contacts": Contacts.objects.all()[0]}
        return render(request, self.template_name, context=context)

    @staticmethod
    def post(request):
        name = request.POST.get("name")

        return HttpResponse(f"Спасибо, {name}! Мы обязательно Вам перезвоним.")
