from __future__ import print_function

import json

from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template import Template
from django.template.loader import get_template
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404

from store.models import Cart, Product, Customer, CartItem
from store.serializers import CustomerSerializer, ProductSerializer, CartSerializer, CartItemSerializer


class CustomerRegistrationView(generics.CreateAPIView):

    EMAIL_SUBJECT = 'Registration Successful'
    serializer_class = CustomerSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'registration-successful-mail.html'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            customer_serializer = self.get_serializer(data=data)
            if customer_serializer.is_valid():
                validate_password(customer_serializer.validated_data.get('password'))
                saved_customer = customer_serializer.save()
                cart = Cart(customer=saved_customer)
                cart.save()
                self.send_notification_successful_mail([saved_customer.email], name=saved_customer.first_name, subject=self.EMAIL_SUBJECT)
                response = {
                    "message": "Sign Up Successful",
                    "data": customer_serializer.data
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED, safe=False)
            else: return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(exception)
            return JsonResponse(f'Registration Unsuccessful, {exception}', status=status.HTTP_400_BAD_REQUEST, safe=False)

    def send_notification_successful_mail(self, to: list, name: str, subject: str):
        msg: EmailMultiAlternatives = EmailMultiAlternatives(subject=subject, to=to)
        msg.attach_alternative(content=self.template_loader(var_dict={'name': name}), mimetype='text/html')
        msg.send()
        print('Message Sent Successfully')


    def template_loader(self, template=None, var_dict: dict = None):
        context = var_dict
        if not template or template is None:
            template: Template = get_template(self.template_name)
            html_content = template.render(context=context)
            return html_content
        else:
            template: Template = get_template(template)
            html_content = template.render(context=context)
            return html_content

class SnapShopProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class SnapShopProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        try:
            product_id = self.kwargs.get('id')
            return Product.objects.get(id=product_id)
        except Exception as exception:
            print(exception)


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            found_product: Product = get_object_or_404(Product, title=data.pop('product_name'))
            customer: Customer = get_object_or_404(Customer, email=data.pop('customer_email'))
            cart, is_created = Cart.objects.get_or_create(customer=customer)
            CartItem.objects.create(product=found_product, cart=cart, quantity=data.pop('quantity'))
            cart_items_serializer = CartItemSerializer(CartItem.objects.filter(cart_id=cart.id), many=True)
            response = {
                "message": "Item Added To Cart",
                "cart": cart_items_serializer.data
            }
            print(response)
            return JsonResponse(response, status=status.HTTP_302_FOUND, safe=False)
        except ValueError as exception:
            print(exception)
            return JsonResponse(f'Exception ==> {exception}', status=status.HTTP_400_BAD_REQUEST, safe=False)

class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()