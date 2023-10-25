from rest_framework import serializers
from .models import Seller, Category, Product, SalesRecord, Buyer, Transaction, Wallet, CardDetails, Cart, History, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, value):
        """
        Validate the email field to ensure it's unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        """
        Create and return a new User instance using the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # Add other fields as needed
        )
        return user

        
class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
        
        def create(self, validated_data):
            images = validated_data.pop("images")
            category = None
            tags = None

class SalesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRecord
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = '__all__'
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    #     extra_kwargs = {
    #         "product": {"required": True},
    #         "quantity": {"required": True, "min_value": 1},
    #     }

    # def get_price(self, obj):
    #     return obj.price

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data["user"] = {
    #         "id": instance.user.id,
    #         "username": instance.user.username,
    #     }
    #     data["product"] = (
    #         {
    #             "id": instance.product.id,
    #             "name": instance.product.name,
    #             "price": instance.product.price,
    #             "images": list(map(lambda x: x.url, instance.product.images)),
    #         }
    #         if instance.product
    #         else None
    #     )

    #     return data

    # def create(self, validated_data):
    #     product = validated_data.get("product")
    #     product_exists_in_cart = Cart.objects.filter(
    #         product__id=product.id
    #     ).exists()

    #     if product_exists_in_cart:
    #         product = Cart.objects.filter(product__id=product.id).first()
    #         product.quantity += 1
    #         product.save()

    #         return product

    #     return super().create(validated_data)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

