from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy

from catalog.forms import ProductForm, ProductModerForm
from catalog.models import Product, Contacts
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View, UpdateView
from django.views.generic.edit import CreateView, DeleteView


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change"] = True

        return context

    def get_form_class(self):
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return ProductModerForm
        else:
            return ProductForm


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
    permission_required = "catalog.delete_product"


class ContactsView(LoginRequiredMixin, View):
    model = Contacts
    template_name = "catalog/contacts_view.html"

    def get(self, request):
        context = {"contacts": Contacts.objects.all()[0]}
        return render(request, self.template_name, context=context)

    @staticmethod
    def post(request):
        name = request.POST.get("name")

        return HttpResponse(f"Спасибо, {name}! Мы обязательно Вам перезвоним.")
