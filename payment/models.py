import enum

from django.db import models

# Create your models here.

class Payment(models.Model):

    class PaymentStatus(enum.Enum):
        PENDING = 'Pending'
        SUCCESSFUL = 'Successful'
        FAILED = 'Failed'

    PAYMENT_STATUS = [
        (status.name, status.value) for status in PaymentStatus
    ]

    class PaymentMethod(enum.Enum):
        CARD = 'Card'
        TRANSFER = 'Transfer'

    PAYMENT_METHOD = [
        (method.name, method.value) for method in PaymentMethod
    ]
    transaction_id = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    payment_status = models.TextField(choices=PAYMENT_STATUS, max_length=10)
    payment_method = models.TextField(choices=PAYMENT_METHOD, max_length=10)