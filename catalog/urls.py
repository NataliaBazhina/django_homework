from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contact, product_list,products_detail

app_name = CatalogConfig.name
urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/<int:pk>/', products_detail, name='products_detail'),
    path("home", home, name="home"),
    path("contacts/", contact, name="contact"),
]
