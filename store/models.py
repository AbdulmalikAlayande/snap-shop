import enum

from django.db import models
from django.db.models import PROTECT, CASCADE, SET_NULL


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_products = models.ForeignKey(to='Product', on_delete=SET_NULL, related_name='+', null=True)

    def __repr__(self):
        return f"""
                    title: {self.title},
                    featured_products: {self.featured_products},
               """

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __repr__(self):
        return f"""
                    description: {self.description},
                    discount: {self.discount}
                """

class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to=Collection, on_delete=PROTECT)
    promotions = models.ManyToManyField(to=Promotion, related_name='products')

    def __repr__(self):
        return  f"""
                    title: {self.title},
                    description: {self.description},
                    price: {self.unit_price},
                    inventory: {self.inventory},
                    last_updated: {self.last_updated}
                    collection: {self.collection}
                    promotions: {self.promotions}
                """

    # Create your models here.

class Customer(models.Model):
    BRONZE_MEMBERSHIP = 'B'
    SILVER_MEMBERSHIP = 'S'
    GOLD_MEMBERSHIP = 'G'
    print(SILVER_MEMBERSHIP)
    print(GOLD_MEMBERSHIP)
    MEMBERSHIP_CHOICES = [
        (BRONZE_MEMBERSHIP, 'Bronze'),
        (SILVER_MEMBERSHIP, 'Silver'),
        (GOLD_MEMBERSHIP, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(error_messages="Invalid Email", unique=True)
    phone_number = models.TextField(max_length=11, null=False)
    profile_image = models.FileField()
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=BRONZE_MEMBERSHIP)
    birth_date = models.DateField(null=True)
    profile_image_url = models.URLField()

    def __repr__(self):
        return  f"""
                    first_name: {self.first_name},
                    last_name: {self.last_name},
                    email: {self.email},
                    phone_number: {self.phone_number},
                    membership: {self.membership}
                    birth_date: {self.birth_date}
                    profile_image_url: {self.profile_image_url}
                """

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['first_name', 'last_name', 'email'])
        ]

class Order(models.Model):
    class Payment_Status(enum.Enum):
        PENDING = 'P',
        COMPLETE = 'C',
        FAILED = 'F'

    PAYMENT_STATUS = [
        (Payment_Status.PENDING, 'Pending'),
        (Payment_Status.COMPLETE, 'Complete'),
        (Payment_Status.FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    payment_status = models.TextField(choices=PAYMENT_STATUS, max_length=1, default=Payment_Status.PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __repr__(self):
        return f"""
                placed_at: {self.placed_at},
                payment_status: {self.payment_status}
                customer_id: {self.customer.id}
                """

class Order_Item(models.Model):
    order = models.ForeignKey(to=Order, on_delete=PROTECT)
    product = models.ForeignKey(to=Product, on_delete=PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

class Address(models.Model):
    city = models.TextField(null=False)
    street = models.TextField(null=False)
    customer = models.OneToOneField(to=Customer, on_delete=CASCADE)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class Item(models.Model):
    order_item = models.ForeignKey(to=Order, on_delete=PROTECT)
    cart = models.ForeignKey(to=Cart, on_delete=PROTECT)

class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
