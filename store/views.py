from django.db.models import QuerySet, Q, F
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product


# Create your views here.

@api_view()
def get_all_products(request):
    product_query_set = Product.objects.all()
    products = []
    for each_prod in product_query_set:
        products.append(each_prod.__repr__())
    return render(request, 'hello1.html', {'products':products})

@api_view()
def get_product(request, product_id: int):
    product = Product.objects.filter(pk=product_id).first()
    return Response(product.__repr__())

@api_view()
def filter_products_by_price(request, product_price: float):
    products: QuerySet[Product] = Product.objects.filter(price=product_price)
    product: QuerySet = products.first()
    return render(request, '', {'product': products})

@api_view()
def filter_products_by_price_range(request, min: float, max: float) -> HttpResponse:
    products_queryset: QuerySet[Product] = Product.objects.filter(unit_price__range=(min, max))
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def filter_using_complex_lookups(request):
    products_queryset = Product.objects.filter(inventory__lt=10, unit_price__gt=20)
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def filter_using_complex_lookups_with_multiple_filter_calls(request):
    products_queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__gt=20)
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def filter_complex_lookups_using_the_Q_object(request):
    products_queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def filter_complex_lookups_by_referencing_fields_with_the_F_object(request):
    products_queryset = Product.objects.filter(inventory=F('collection__id'))
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def filter_by_model_relationship(request):
    products_queryset = Product.objects.filter(collection__featured_products_id__gt=10)
    print(list(products_queryset))
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})
