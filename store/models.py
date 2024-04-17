import enum
import json
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from address.models import AddressField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT, CASCADE

from payment.models import Payment

class AbstractModel(models.Model):
    id = models.UUIDField(
        verbose_name=_('Id'),
        default=uuid.uuid4(),
        unique=True,
        editable=False,
        db_index=True
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    class Meta:
        abstract = True
        ordering = []
        verbose_name = _('Abstract Model')
        verbose_name_plural = _('Abstract Models')

class User(AbstractModel, AbstractBaseUser):
    email = models.EmailField(_('Email'), max_length=100, unique=True, db_index=True, blank=False, null=False)
    full_name = models.CharField(_('Name'), max_length=40, blank=True)
    password = models.CharField(_('Password'), max_length=20, blank=False, null=False)
    is_active = models.BooleanField(_('Active'), help_text=_('Designates Whether A User Can Access Their Account'), default=True)
    is_admin = models.BooleanField(_('Admin'), help_text=_('Designates Whether A User Can log into the admin site'))
    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_permission(self):
        return self.is_active and self.is_admin

    def get_all_permissions(self, obj=None):
        return []

    class Meta(AbstractModel.Meta):
        verbose_name = _('User Model')
        verbose_name_plural = _('User Models')

class Product(models.Model, AbstractModel):
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

    def __str__(self):
        return  f"""{self.title} ({self.description})"""

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    class Meta:
        db_table = 'products'

class Customer(AbstractUser):
    phone_number = models.TextField(max_length=11, null=False)
    birth_date = models.DateField(null=True)
    address = AddressField(related_name='+', blank=True, null=True)

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        # address = list(self.address) if isinstance(self.address, set) else self.address
        data =   {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'address': self.address
        }
        return json.dumps(data, indent=4)

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

    def __str__(self):
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

    def __str__(self):
        return f"""customer: {self.customer}
        created_at: {self.created_at}
        """

    class Meta:
        db_table = 'carts'

class CartItemManager(models.Manager):

    def create(self, **kwargs):
        quantity = kwargs.get('quantity')
        item = self.filter(kwargs.get('cart'), kwargs.get('product'))
        if item.exists():
            item.first().quantity = item.first().quantity + quantity
            return super().update(item)
        else: return super().create(kwargs)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    objects = CartItemManager()

    class Meta:
        db_table = 'cart items'

class Rating(models.Model):
    product = models.ForeignKey(to=Product, on_delete=CASCADE)
    customer = models.ForeignKey(to=Customer, on_delete=CASCADE)
    reviewText = models.TextField(max_length=1000)
    datetime = models.DateTimeField()

    class Meta:
        db_table = 'ratings'