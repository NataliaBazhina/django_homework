from itertools import product

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.models import Product


def home(request):
    return render(request, "home.html")


# def contact(request):
#     return render(request, "contact.html")

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product

class ContactView(TemplateView):
    template_name = "catalog/contact.html"

class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')