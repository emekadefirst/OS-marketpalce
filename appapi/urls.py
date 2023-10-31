from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_view, name="login"),
    path('test', views.test_token, name="test"),
    path('all-products', views.all_product, name="all-product"),
    path('register', views.register_user, name="register"),
    path('create-seller', views.create_seller, name="create-seller"),
    path('products/<str:model_name>/<int:pk>/',
         views.product_detail, name='product_detail'),
    path('add-product', views.addProduct, name="upload_product"),
    path('', views.home, name="home-page"),
    path('search/', views.search, name='search'),
    path('cart_view', views.cart_view, name="cart_view")
]


