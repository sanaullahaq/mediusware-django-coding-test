from django.views import generic
from product.models import Variant, ProductVariantPrice
from django.shortcuts import render, redirect
from django.db.models import Q


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListView(generic.ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'product_variant_prices'
    paginate_by = 2
    queryset = ProductVariantPrice.objects.all()


def is_valid_parameter(param):
    return param != "" and param is not None


def list_filtered(request):
    qs = ProductVariantPrice.objects.all()

    title = request.GET.get('title')
    variant = request.GET.get('variant')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    date = request.GET.get('date')

    if is_valid_parameter(title):
        qs = qs.filter(product__title__icontains=title)
    if is_valid_parameter(variant) and variant != '--Select A Variant--':
        qs = qs.filter(
            Q(product_variant_one__variant_title__icontains=variant) |
            Q(product_variant_two__variant_title__icontains=variant)
        )
    if is_valid_parameter(price_from):
        qs = qs.filter(price__gte=price_from)

    if is_valid_parameter(price_to):
        qs = qs.filter(price__lte=price_to)

    if is_valid_parameter(date):
        qs = qs.filter(product__created_at__gte=date)

    return render(request, 'products/list.html', {'product_variant_prices': qs})
