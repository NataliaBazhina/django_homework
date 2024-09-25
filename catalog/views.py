from itertools import product

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView

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