import enum

from django.db import models
from django.db.models import PROTECT, CASCADE, SET_NULL


# Create your models here.
class Item(models.Model):
    pass

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_products = models.ForeignKey(to='Product', on_delete=SET_NULL, related_name='+', null=True)

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to=Collection, on_delete=PROTECT)
    promotions = models.ManyToManyField(to=Promotion, related_name='products')

    def __repr__(self):
        return f"""
            {
                'title': {self.title},
                description: {self.description},
                price: {self.price},
                inventory: {self.inventory},
                last_updated: {self.last_updated}
            }
        """

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
    item = models.ForeignKey(to=Item, on_delete=PROTECT)

    def __repr__(self):
        return f"""
            {
                'placed_at': {self.placed_at},
                payment_status: {self.payment_status}
            }
        """

class Order_Item(models.Model):
    order = models.ForeignKey(to=Order, on_delete=PROTECT)
    product = models.ForeignKey(to=Product, on_delete=PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

class Customer(models.Model):
    class Membership_Type(enum.Enum):
        BRONZE_MEMBERSHIP = 'B',
        SILVER_MEMBERSHIP = 'S',
        GOLD_MEMBERSHIP = 'G'
    MEMBERSHIP_CHOICES = [
        (Membership_Type.BRONZE_MEMBERSHIP, 'Bronze'),
        (Membership_Type.SILVER_MEMBERSHIP, 'Silver'),
        (Membership_Type.GOLD_MEMBERSHIP, 'Gold')
    ]
    first_name = models.TextField(max_length=255, null=False)
    last_name = models.TextField(max_length=255, null=False)
    email = models.EmailField(error_messages="Invalid Email", unique=True)
    phone_number = models.TextField(max_length=11, null=False)
    profile_image = models.FileField()
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=Membership_Type.BRONZE_MEMBERSHIP)
    birth_date = models.DateField(null=True)
    profile_image_url = models.URLField()
    order = models.ForeignKey(to=Order, on_delete=PROTECT)

    def __repr__(self):
        return f"""
            {
                'first_name': {self.first_name},
                last_name: {self.last_name},
                email: {self.email},
                phone_number: {self.phone_number},
                membership: {self.membership}
                birth_date: {self.birth_date}
                profile_image_url: {self.profile_image_url}
            }
        """

    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['first_name', 'last_name', 'email'])
        ]

class Address(models.Model):
    city = models.TextField(null=False)
    street = models.TextField(null=False)
    customer = models.OneToOneField(to=Customer, on_delete=CASCADE)

class Cart(models.Model):
    item = models.ForeignKey(to=Item, on_delete=PROTECT)

class Cart_Item(models.Model):
    pass

