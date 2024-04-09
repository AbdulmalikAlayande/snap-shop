from __future__ import print_function

import json

from django.contrib.auth.password_validation import validate_password
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.template import Template
from django.template.loader import get_template
from rest_framework import status, generics

from store.models import Cart
from store.serializers import CustomerSerializer


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
