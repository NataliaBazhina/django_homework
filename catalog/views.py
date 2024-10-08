from itertools import product

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Version


def home(request):
    return render(request, "home.html")


# def contact(request):
#     return render(request, "contact.html")

class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_versions = product.versions.filter(version_flag=True)
        context['active_versions'] = active_versions
        return context

class ContactView(TemplateView):
    template_name = "catalog/contact.html"

class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['product_name'].lower()
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                form.add_error('product_name', 'Данное название не подходит.')
                return self.form_invalid(form)

        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'product_description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')