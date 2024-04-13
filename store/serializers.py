from address.models import Country, State, Locality
from rest_framework import serializers

from store.models import Customer, Product, Cart, CartItem


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=3)

    class Meta:
        model = Country
        fields = ['street_number', 'route', 'locality']

class StateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=3)
    country = serializers.RelatedField(queryset=Country.objects.all())

    class Meta:
        model = State
        fields = ['street_number', 'route', 'locality']

class LocalitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=15)
    postal_code = serializers.CharField(max_length=10)
    state = serializers.RelatedField(queryset=State.objects.all())

    class Meta:
        model = Locality
        fields = ['street_number', 'route', 'locality']

# class AddressSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Address
#         fields = ['street_number', 'route', 'locality']
#
    # def  create(self, validated_data):
    #     print('hello')
    #     if validated_data:
    #         created_address = Address.objects.create(**validated_data)
    #         return created_address

class CustomerSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    username = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=11)
    birth_date = serializers.DateField(required=False, format='%d-%m-%Y')

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'username', 'birth_date']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class ProductSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=255, allow_null=False)
    description = serializers.CharField(allow_null=False)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)
    category = serializers.CharField(allow_null=False)
    last_updated = serializers.DateTimeField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price', 'quantity', 'category', 'last_updated']

class OrderSerializer(serializers.Serializer):
    pass

class OrderItemSerializer(serializers.Serializer):
    pass

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=30, required=True)
    quantity = serializers.IntegerField(min_value=0, required=True)
    customer_email = serializers.CharField(max_length=30, required=True)
    message = serializers.CharField(max_length=255)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'customer', 'quantity', 'product_name', 'customer_email', 'message']
        read_only_fields = ['id', 'message']
        write_only_fields = []


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=0)
    item_name = serializers.CharField(source='product.title', max_length=20)
    item_description = serializers.CharField(source='product.description', max_length=300)
    item_price = serializers.DecimalField(source='product.unit_price', max_digits=10, decimal_places=2)
    item_category = serializers.CharField(source='product.category', max_length=10)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'quantity', 'item_name', 'item_description', 'item_price', 'item_category']
        read_only_fields = ['item_name', 'item_description', 'item_price', 'item_category']
        extra_kwargs = {
            'item_name': {'read_only': True},
            'item_description': {'read_only': True},
            'item_price': {'read_only': True},
            'item_category': {'read_only': True}
        }

class RatingSerializer(serializers.Serializer):
    pass