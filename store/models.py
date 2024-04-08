import enum
import json

from address.models import AddressField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT, CASCADE

from payment.models import Payment


class Product(models.Model):

    class ProductCategory(enum.Enum):
        KIDS = 'Kids'
        ADULTS = 'Adults'
        FOOD = 'Food'
        KITCHEN = 'Kitchen'
        FASHION = 'Fashion'
        SPORTS = 'Sports'

    PRODUCT_CATEGORY = [
        (category.value, category.name) for category in ProductCategory
    ]

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    category = models.TextField(choices=PRODUCT_CATEGORY)
    last_updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return  f"""
                    title: {self.title},
                    description: {self.description},
                    price: {self.unit_price},
                    inventory: {self.quantity},
                    category: {self.category},
                    last_updated: {self.last_updated}
                """


class Customer(AbstractUser):
    phone_number = models.TextField(max_length=11, null=False)
    birth_date = models.DateField(null=True)
    address = AddressField(related_name='+', blank=True, null=True)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return  f"""
                    first_name: {self.first_name}
                    last_name: {self.last_name}
                    email: {self.email}
                    password: {self.password}
                    phone_number: {self.phone_number}
                    birth_date: {self.birth_date}
                    address: {self.address}
                """

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['first_name', 'last_name', 'email'])
        ]

class Order(models.Model):
    class OrderStatus(enum.Enum):
        DELIVERED = 'Delivered'
        PENDING = 'Pending'
        EN_ROUTE = 'En route'

    ORDER_STATUS = [
        (status.name, status.value) for status in OrderStatus
    ]
    placed_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    order_number = models.PositiveIntegerField()
    order_status = models.TextField(choices=ORDER_STATUS, max_length=10, default=OrderStatus.PENDING.value)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    payment = models.OneToOneField(to=Payment, on_delete=CASCADE)

    def __repr__(self):
        return f"""
                placed_at: {self.placed_at},
                order_status: {self.order_status}
                order_number: {self.order_number}
                customer_id: {self.customer.id}
                total_price: {self.total_price}
                payment: {self.payment}
                """

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=PROTECT)
    product = models.ForeignKey(to=Product, on_delete=PROTECT)
    quantity = models.PositiveIntegerField()

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.OneToOneField(to=Customer, on_delete=CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

class Rating(models.Model):
    product = models.ForeignKey(to=Product, on_delete=CASCADE)
    customer = models.ForeignKey(to=Customer, on_delete=CASCADE)
    reviewText = models.TextField(max_length=1000)
    datetime = models.DateTimeField()