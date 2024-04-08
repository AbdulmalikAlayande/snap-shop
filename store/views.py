import json

from django.contrib.auth.hashers import Argon2PasswordHasher
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework import status, generics

from store.serializers import CustomerSerializer


class CustomerRegistrationView(generics.CreateAPIView):

    serializer_class = CustomerSerializer
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        customer_serializer = self.get_serializer(data=data)
        if customer_serializer.is_valid():
            validate_password(customer_serializer.validated_data.get('password'))
            customer_serializer.save()
            response = {
                "message": "Sign Up Successful",
                "data": customer_serializer.data
            }
            return JsonResponse(response, status=status.HTTP_201_CREATED, safe=False)
        else: return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)