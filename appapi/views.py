from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Seller, Product, Category, SalesRecord, Cart
from .serializers import BuyerSerializer, SellerSerializer, CategorySerializer, ProductSerializer, CartSerializer
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.dispatch import receiver
from .serializers import OrderSerializer
from .models import Order, Buyer
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow registration for unauthenticated users
def register_user(request):
    if request.method == 'POST':
        data = request.data  # Assuming you send a JSON request with the provided data

        # Use the BuyerSerializer for registration
        serializer = BuyerSerializer(data=data)

        if serializer.is_valid():
            # Extract user-related data from the request
            user_data = {
                'username': data['username'],
                'password': data['password'],
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone_number': data['phone_number'],
            }

            # Create the user
            user = User.objects.create_user(**user_data)

            # Create the Buyer instance associated with the user
            buyer = Buyer(user=user, phone_number=data['phone_number'])
            buyer.save()

            # Create a token for the user
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user': BuyerSerializer(buyer).data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    serializer = BuyerSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

# Seller creation view
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

# List all products view
@api_view(['GET'])
def all_product(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Specific product view
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

# Search view
@api_view(['GET', 'POST'])
def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(ID__icontains=query) |
        Q(product_description__icontains=query) |
        Q(category__icontains=query)
    )

    if not results:
        return Response({"Error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    results_data = [{'name': item.name, 'product_description': item.product_description, 'category': item.category} for item in results]

    return Response(results_data, status=status.HTTP_200_OK)

# User profile view
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request):
    user = request.user  # Get the authenticated user

    if user is not None:
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # Add more user-related fields as needed

            # Additional fields from the Buyer model
            'phone_number': user.buyer_set.first().phone_number,
            'profile_image': user.buyer_set.first().profile_image.url if user.buyer_set.first().profile_image else None,
            'wallet_balance': user.buyer_set.first().wallet.balance,
            'street_address': user.buyer_set.first().street_address,
            'land_mark': user.buyer_set.first().land_mark,
            'date_created': user.buyer_set.first().date_created,
            'LGA': user.buyer_set.first().LGA,
            'state': user.buyer_set.first().state,
            # Add more Buyer model fields as needed

            # Include Wallet data
            'wallet_transactions': [
                {
                    'amount': transaction.amount,
                    'status': transaction.status,
                    'type': transaction.type,
                    # Add more Wallet transaction fields as needed
                }
                for transaction in user.buyer_set.first().wallet.transaction_set.all()
            ],

            # Include History data
            'purchase_history': [
                {
                    'total_purchase': history.total_purchase,
                    'time_purchased': history.time_purchased,
                    # Add more History fields as needed
                }
                for history in user.buyer_set.first().history_set.all()
            ],
        }

        return Response(user_data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# View for handling the user's shopping cart
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Use IsAuthenticated to ensure the user is logged in
def cart_view(request):
    if request.method == 'GET':
        # Retrieve all items in the user's cart
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new item in the user's cart
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user  # Associate the item with the logged-in user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import login
from allauth.account.models import EmailAddress
from allauth.account.views import SignupView
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

@require_POST
def custom_signup_view(request):
    # Instantiate the SignupView and process the form data
    signup_view = SignupView()
    signup_view.request = request
    form = signup_view.get_form(signup_view.form_class)

    if form.is_valid():
        response = signup_view.form_valid(form)

        # Log the user in immediately after registration
        login(request, signup_view.user)

        # Send an email verification link to the user
        email_address = EmailAddress.objects.get(user=signup_view.user)
        email_address.send_confirmation(request)

        return response

    # If the form is not valid, return an error response or redirect as needed
    # Example: return render(request, 'registration/signup.html', {'form': form})
    return HttpResponseRedirect('/registration/error/')  # Redirect to an error page if the form is not valid

