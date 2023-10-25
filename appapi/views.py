from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Seller, Product, Category, SalesRecord
from .serializers import UserSerializer, SellerSerializer, CategorySerializer, ProductSerializer
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@api_view(['POST'])
@csrf_exempt
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

# Login view


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email).first()

    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_seller(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Seller created successfully"}, status=201)
    return JsonResponse(serializer.errors, status=400)


# Test token view


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

# List all products view


@receiver(user_logged_in)
def update_last_login_timestamp(sender, request, user, **kwargs):
    user.last_login_timestamp = user.last_login
    user.save()


from rest_framework import permissions

class IsSellerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a seller.
        return request.user and request.user.is_authenticated and hasattr(request.user, 'seller')


@api_view(['GET'])
def all_product(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specific_product(request, model_name, pk):
    return Response({"Success": "Access granted"}, status=200)

# Add product view


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsSellerPermission]) 
def addProduct(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    return Response("Method not allowed for GET request", status=405)


# Product detail view (GET, PUT, DELETE)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsSellerPermission]) 
def product_detail(request, model_name, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)

# Create sales record view


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSellerPermission]) 
def create_sales_record(request):
    if request.method == 'POST':
        # Assuming you have authenticated the seller and retrieved them as some_authenticated_seller
        # Assuming you have identified the product as some_product
        some_authenticated_seller = request.user
        # Assuming 'product_id' is a key in the request data
        some_product_id = request.data.get('product_id')

        # Retrieve the product object based on the product ID
        try:
            some_product = Product.objects.get(pk=some_product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new sales record
        new_sale = SalesRecord(
            seller=some_authenticated_seller,
            product=some_product,
            quantity_sold=10,
            total_sales=100.00
        )
        new_sale.save()

        return Response("Sale recorded successfully")

    return Response("Method not allowed for GET request", status=405)

# Home view


@api_view(['GET'])
def home(request):
    return Response("ok")
