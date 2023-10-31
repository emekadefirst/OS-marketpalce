import secrets
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

def generate_reference():
    return secrets.token_hex(8).upper()

class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    phone_number = models.CharField(max_length=15)
    profile_image = models.FileField(upload_to="buyer-img-store")
    wallet_balance = models.FloatField(max_length=8, default=0.00)
    street_address = models.TextField(default=None)
    land_mark = models.TextField(default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    LGA = models.CharField(max_length=50)
    state = models.CharField(max_length=15)
    username = models.CharField(max_length=150)  # Add this field

    def __str__(self):
        return self.username

class Seller(models.Model):
    user = models.OneToOneField(Buyer, on_delete=models.CASCADE, null=True, default=None)
    Identity_Type = (
        ('School', 'SCHOOL-ID-CARD'),
        ('Faculty', 'FACULTY-ID-CARD'),
    ) 
    Identity = models.CharField(
        max_length=10,
        choices=Identity_Type,
        default='SCHOOL-ID-CARD',
    )
    National_ID_Number = models.IntegerField(default='')
    id_image = models.FileField(upload_to="ID-img-store")
    matric_number = models.CharField(max_length=50, unique=True, default='')
    university_name = models.CharField(max_length=300)
    faculty = models.CharField(max_length=300)
    department = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login_timestamp = models.DateTimeField(null=True, blank=True)  # Added field

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_created']

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='customuser_set',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='customuser_set',
        related_query_name='user',
    )

class Category(models.Model):
    name = models.CharField(max_length=250)
    product_count = models.PositiveIntegerField(default=0)  # Add this field

    class Meta:
        permissions = [
            ("view_category_custom", "Can view categories"),
            ("add_category_custom", "Can add categories"),
            ("change_category_custom", "Can change categories"),
            ("delete_category_custom", "Can delete categories"),
        ]

        
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=350)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.FileField(upload_to="Product-img-store")
    date_created = models.DateTimeField(auto_now_add=True)
    product_description = models.TextField(default='')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("view_product_custom", "Can view products"),
            ("add_product_custom", "Can add products"),
            ("change_product_custom", "Can change products"),
            ("delete_product_custom", "Can delete products"),
        ]
        ordering = ['-date_created']

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    # Link to the CustomUser model
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    # Assuming a Product model for the sold product
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    time_sold = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SalesRecord for {self.seller} - {self.product} at {self.time_sold}"


    
class Transaction(models.Model):
    class TRANSACTION_STATUS(models.TextChoices):
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        PENDING = "PENDING", "Pending"
        FAILED = "FAILED", "Failed"

    class TRANSACTION_TYPE(models.TextChoices):
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    user = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=TRANSACTION_STATUS.choices,
        default=TRANSACTION_STATUS.PENDING,
    )
    type = models.CharField(max_length=50, choices=TRANSACTION_TYPE.choices)
    reference = models.CharField(max_length=50, default=generate_reference)
    platform_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Transaction"

    # class Meta:
    #     ordering = ["-created_at"]
    
class Wallet(models.Model):
    user = models.OneToOneField(Buyer, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    # class Meta:
    #     ordering = ["-created_at"]

    
class CardDetails(models.Model):
    card_type = (
            ('VISA', 'VISA-CARD'),
            ('MASTERCARD', 'MASTERCARD'),
    )
    card_owner = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, default=None)
    card = models.CharField(max_length=10, choices=card_type, default=None)
    card_name = models.CharField(max_length=30)
    card_number = models.IntegerField()
    cvc = models.IntegerField()
    pin = models.IntegerField()

class Cart(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    time_added = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    time_purchased = models.DateTimeField(auto_now_add=True)
    

   
class Order(models.Model):
    class ORDER_STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    reference = models.CharField(max_length=50, default=generate_reference)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS.choices, default=ORDER_STATUS.PENDING
    )





