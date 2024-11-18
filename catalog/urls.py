from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import home, ContactView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='products_detail'),
    path("home", home, name="home"),
    path("contacts/", ContactView.as_view(), name="contact"),
    path('create/', ProductCreateView.as_view(), name = 'create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name = 'update_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name = 'delete_product'),
]
