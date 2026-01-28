from django.urls import path
from . import views
from .views import orders

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.place_order, name='place_order'),
    path('cart/', views.cart, name='cart'),
    path('cart/increase/<str:key>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<str:key>/', views.decrease_quantity, name='decrease_quantity'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order-success/', views.order_success, name='order_success'),
    path('category/<int:category_id>/', views.product_list, name='category_filter'),

]