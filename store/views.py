import json

from address.models import Address
from django.http import JsonResponse
from django.views.generic.edit import BaseCreateView
from rest_framework import status, generics

from store.models import Customer
from store.serializers import CustomerSerializer, AddressSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    serializer_class = CustomerSerializer

    # def post(self, request, *args, **kwargs):
    #     data = json.loads(request.body)
    #     customer_serializer = self.get_serializer(data=data)
    #     address_serializer = AddressSerializer(data=data.pop('address', None))
    #     if customer_serializer.is_valid:
    #         customer = customer_serializer.save(commit=False)
    #
    #     return JsonResponse('', status=status.HTTP_201_CREATED)