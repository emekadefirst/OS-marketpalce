from django.contrib import admin
from .models import Seller, Category, Product, SalesRecord, Buyer, Transaction, Wallet, CardDetails, Cart, History, Order

class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'matric_number', 'university_name', 'faculty', 'department', 'phone_number']
    list_filter = ['university_name', 'faculty', 'department']
    search_fields = ['user__username', 'matric_number']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'seller']
    list_filter = ['category', 'seller']
    search_fields = ['name']

class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ['seller', 'product', 'quantity_sold', 'total_sales', 'time_sold']
    list_filter = ['seller', 'product']
    search_fields = ['seller__user__username', 'product__name']

class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'wallet_balance', 'LGA', 'state']
    list_filter = ['LGA', 'state']
    search_fields = ['user__username']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'amount', 'status', 'type', 'reference', 'platform_reference']
    list_filter = ['status', 'type']
    search_fields = ['user__user__username', 'reference']

class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

class CardDetailsAdmin(admin.ModelAdmin):
    list_display = ['card_owner', 'card', 'card_name', 'card_number']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'cost', 'quantity', 'time_added']

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart', 'total_purchase', 'time_purchased']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'reference', 'transaction', 'status']

admin.site.register(Seller, SellerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SalesRecord, SalesRecordAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(CardDetails, CardDetailsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Order, OrderAdmin)
