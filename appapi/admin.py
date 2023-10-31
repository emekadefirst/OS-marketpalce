from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Seller, Category, Product, SalesRecord, Buyer, Transaction, Wallet, CardDetails, Cart, History, Order

class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'matric_number', 'university_name', 'faculty', 'department', 'date_created')
    search_fields = ('user__username', 'matric_number', 'university_name', 'faculty', 'department')
    list_filter = ('university_name', 'faculty')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    list_filter = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'date_created')
    search_fields = ('name', 'category__name', 'price', 'quantity')
    list_filter = ('category', 'price')

class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('seller', 'product', 'quantity_sold', 'total_sales', 'time_sold')
    search_fields = ('seller__user__username', 'product__name', 'quantity_sold', 'total_sales')
    list_filter = ('product',)

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'wallet_balance', 'date_created')
    search_fields = ('user__username', 'phone_number', 'wallet_balance')
    list_filter = ('user__username', 'wallet_balance')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'type', 'reference')
    search_fields = ('user__username', 'amount', 'status', 'type', 'reference')
    list_filter = ('status', 'type')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'balance')
    list_filter = ('balance',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'cost', 'quantity', 'time_added')
    search_fields = ('user__username', 'product__name', 'cost', 'quantity')
    list_filter = ('cost', 'quantity')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'total_purchase', 'time_purchased')
    search_fields = ('user__username', 'cart__product__name', 'total_purchase')
    list_filter = ('total_purchase',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'reference', 'status')
    search_fields = ('user__username', 'product__name', 'quantity', 'reference', 'status')
    list_filter = ('status',)

admin.site.register(Seller, SellerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SalesRecord, SalesRecordAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(CardDetails)
admin.site.register(Cart, CartAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Order, OrderAdmin)
