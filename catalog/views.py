from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
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
    form_class = ProductModerForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change"] = True

        return context

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductModerForm
        else:
            raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user != self.object.owner and not user.has_perm(
            "catalog.can_unpublish_product"
        ):
            raise PermissionDenied
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if not self.request.user.has_perm(
            "catalog.can_unpublish_product"
        ) and self.request.user != form.cleaned_data.get("owner"):
            raise PermissionDenied
        return super().form_valid(form)


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
