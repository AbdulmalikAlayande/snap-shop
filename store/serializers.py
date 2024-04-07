from address.models import Address, Country, State, Locality
from rest_framework import serializers

from store.models import Customer


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

class AddressSerializer(serializers.ModelSerializer):


    class Meta:
        model = Address
        fields = ['street_number', 'route', 'locality']

    def  create(self, validated_data):
        print('hello')
        if validated_data:
            created_address = Address.objects.create(**validated_data)
            return created_address

class CustomerSerializer(serializers.Serializer):
    address = AddressSerializer(required=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=30)
    password = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=11)
    profile_image = serializers.FileField(required=False)
    birth_date = serializers.DateField(required=False)
    profile_image_url = serializers.URLField(required=False)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'profile_image', 'birth_date', 'profile_image_url', 'address']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'write_only': True},
        }

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        customer = Customer.objects.create(**validated_data)
        print('HI')
        if address_data:
            Address.objects.create(**address_data)
        return customer
class ProductSerializer(serializers.Serializer):
    pass

class OrderSerializer(serializers.Serializer):
    pass

class OrderItemSerializer(serializers.Serializer):
    pass

class CartSerializer(serializers.Serializer):
    pass

class CartItemSerializer(serializers.Serializer):
    pass

class RatingSerializer(serializers.Serializer):
    pass