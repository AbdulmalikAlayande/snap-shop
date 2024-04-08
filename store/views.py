import json
import os

from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from requests import Response
from rest_framework import status, generics
import requests

from store.models import Cart
from store.serializers import CustomerSerializer


class CustomerRegistrationView(generics.CreateAPIView):

    serializer_class = CustomerSerializer
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            customer_serializer = self.get_serializer(data=data)
            if customer_serializer.is_valid():
                validate_password(customer_serializer.validated_data.get('password'))
                saved_customer = customer_serializer.save()
                cart = Cart(customer=saved_customer)
                cart.save()
                self.send_notification_successful_mail(customer_serializer.validated_data.get('email'))
                response = {
                    "message": "Sign Up Successful",
                    "data": customer_serializer.data
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED, safe=False)
            else: return JsonResponse(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            print(exception)
            return JsonResponse(f'Registration Unsuccessful, {exception}', status=status.HTTP_400_BAD_REQUEST, safe=False)

    def send_notification_successful_mail(self, email: str) -> object:
        """

        :param email:
        :return: the response from the request object
        """
        print('Hello')
        payload = {
            "from":"alaabdulmalik03@gmail.com",
            "to": email,
            "subject": "Registration Successful Mail",
            "text":"Your Registration Was Successful",
        }
        url = 'https://api.brevo.com/v1/email/send'
        headers = {
            'api-key': os.environ.get('BREVO_API_KEY'),
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        response: Response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        return response