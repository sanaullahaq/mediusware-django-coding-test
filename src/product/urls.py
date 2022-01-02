from django.urls import path
from django.views.generic import TemplateView
from product.models import *
from product.views.product import CreateProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView
from product import views

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'product': True,
        'product_variant_prices': ProductVariantPrice.objects.all(),
    }), name='list.product'),

    path('list_filtered/', views.product.list_filtered, name='list_filtered'),
]
