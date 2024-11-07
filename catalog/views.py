from itertools import product

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from catalog.forms import VersionForm, ProductForm
from catalog.models import Product, Version


def home(request):
    return render(request, "home.html")


# def contact(request):
#     return render(request, "contact.html")

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(is_active = True)


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

class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['product_name'].lower()
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                form.add_error('product_name', 'Данное название не подходит.')
                return self.form_invalid(form)
        form.owner = self.request.user
        return super().form_valid(form)

    # product = form.save()
    # user = self.request.user
    # product.owner = user
    # product.save()
    # return super().form_valid(form)



class ProductUpdateView(UpdateView, PermissionRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")
    permission_required = 'catalog.change_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm,extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST,instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))




class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')