from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart-view/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart , name='remove'),
    path('increase-decrease/<int:pk>/<type>', views.increase_decrease , name='increase-decrease'),
    path('cancel/<int:id>/', views.cancel_order, name='cancel-order'),
    path('remove/<int:id>/', views.remove_order, name='remove-order'),
    path('remove-order/<int:id>/', views.remove_order_by_admin, name='remove-order-admin'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('update-order-status/<int:id>/', views.UpdateOrdersView.as_view(), name='update-order-status'),
    path('orders/export/', views.export_orders_to_excel, name='export_orders_to_excel'),

]