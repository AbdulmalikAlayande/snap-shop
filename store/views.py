from __future__ import print_function

import json

from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.template import Template
from django.template.loader import get_template
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError

from store.models import Cart, Product, Customer, CartItem
from store.serializers import (CustomerSerializer, ProductSerializer,
                               CartSerializer, CartItemSerializer,
                               RemoveCartItemSerializer)
from store.utils import get_object_or_404


class CustomerRegistrationView(generics.CreateAPIView):

    EMAIL_SUBJECT = 'Registration Successful'
    serializer_class = CustomerSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'registration-successful-mail.html'

    def post(self, request, *args, **kwargs):
        customer_serializer = self.get_serializer(data=json.loads(request.body))
        try:
            if customer_serializer.is_valid():
                validate_password(customer_serializer.validated_data.get('password'))
                saved_customer = customer_serializer.save()
                cart = Cart(customer=saved_customer)
                cart.save()
                self.send_notification_successful_mail([saved_customer.email], name=saved_customer.first_name, subject=self.EMAIL_SUBJECT)
                data = {
                    "message": "Sign Up Successful",
                    "data": customer_serializer.data
                }
                return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
            else: return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            data = {
                "message": "Registration Unsuccessful",
                "cause": exception.args,
                "cause__str": str(exception)
            }
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST, safe=False)

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

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
    
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
            return JsonResponse(response, status=status.HTTP_302_FOUND, safe=False)
        except Exception as exception:
            response = {
                "message": "Item Could Not Be be Added To Cart",
                "cause": exception.args
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)

class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

class RemoveFromCartView(generics.DestroyAPIView):
    serializer_class = RemoveCartItemSerializer

    def delete(self, request, *args, **kwargs):
        cart_item_serializer = self.get_serializer(data=json.loads(request.body))
        try:
            cart_item_serializer.is_valid(raise_exception=True)
            customer = get_object_or_404(Customer, email=cart_item_serializer.validated_data.get("customer_email"))
            customers_cart = get_object_or_404(Cart, customer=customer)
            product_name = cart_item_serializer.validated_data.get("product_name")
            CartItem.objects.filter(Q(cart=customers_cart) & Q(product__title=product_name)).delete()
            data = {
                "message": "%s Was Deleted From Your Cart" % product_name,
                "cart": list(CartItem.objects.filter(cart=customers_cart))
            }
            print(data)
            return JsonResponse(data=data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as exception:
            errors_dict = {}
            for argument in exception.args:
                for error in argument:
                    errors_list = list(map(str, argument.get(error)))
                    errors_dict[error] = errors_list
            return JsonResponse(data=errors_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            errors = {
                'message': 'Error Removing Item from Cart',
                "cause": exception.args
            }
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)