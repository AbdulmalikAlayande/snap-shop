from django.db.models import QuerySet, Q, F, Func, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store.models import Product, Customer, Order


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
def get_sorted_products(request):
    #Get products by title in descending order
    products_queryset1 = Product.objects.order_by('title').reverse()
    #Get products by title in ascending order and unit price in descending order
    products_queryset2 = Product.objects.order_by('title', '-unit_price')
    #Get products by title in ascending order and returning the first object
    products_queryset3 = Product.objects.order_by('title').earliest('title')
    #Get the first product from the list of all products sorted by title
    products_queryset4 = Product.objects.earliest('title')
    #Get the last product from the list of all products sorted by title
    products_queryset5 = Product.objects.latest('title')

    print('p1 ==>', products_queryset1)
    print('p2 ==>', products_queryset2)
    print('p3 ==>', products_queryset3.__repr__())
    print('p4 ==>', products_queryset4.__repr__())
    print('p5 ==>', products_queryset5.__repr__())
    return render(request, 'hello1.html')

def select_fields_to_query(request):
    values = Product.objects.values()
    values_list = Product.objects.values_list()
    print(values_list)
    return render(request, 'hello1.html', {'values': values, 'values_list': list(values_list)})


@api_view()
def filter_by_model_relationship(request):
    products_queryset = Product.objects.filter(collection__featured_products_id__gt=10)
    print(list(products_queryset))
    return render(request, 'view_for_lists.html', {'products': list(products_queryset)})

@api_view()
def get_customers_with_dot_com_account(request: HttpRequest) -> HttpResponse:
    customers_query_set = Customer.objects.filter(email__endswith='.com').values()
    print(len(list(customers_query_set)))
    return render(request, 'view_for_lists.html', {'products': list(customers_query_set)})

def get_orders_placed_by_customer_with_id_1(request):
    orders_placed = Order.objects.filter(customer_id=1)
    print(orders_placed)
    return render(request, 'view_for_lists.html', {'products': list(orders_placed)})

def annotate_customer_table_with_new_fields(request):
    annotated_customers_query_set = Customer.objects.annotate(new_id=F('id')+20)
    print(annotated_customers_query_set)
    return render(request, 'view_for_lists.html', {'products': list(annotated_customers_query_set)})

def concat_fields_in_a_database_table(request):
    customers = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    customers2 = Customer.objects.annotate(full_name=Concat('first_name', Value(' '),'last_name'))
    customers_list = [list(customers), list(customers2)]
    print(customers)
    print('===============================================')
    print(customers2)
    print('===============================================')
    print(customers_list)
    return render(request, 'view_for_lists.html', {'products': customers_list})
