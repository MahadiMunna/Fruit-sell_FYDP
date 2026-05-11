from django.urls import path
from . import views

urlpatterns = [
    path('', views.available_fruits, name='fruits'),
    path('fruit_details/<int:id>/', views.DetailFruitView.as_view(), name='details'),

    path('add_fruit', views.add_fruit, name='add_fruit'),
    path('edit_fruit/<int:id>/', views.EditFruitView.as_view(), name='edit_fruit'),
    path('add_vendor', views.add_vendor, name='add_vendor'),

    path('stocked_out/<int:id>/', views.make_stocked_out, name='stocked_out'),
    path('archive_fruits/', views.archive_fruits, name='archive'),
    path('move_to_regular/<int:id>/', views.move_to_regular, name='move_to_regular'),
    path('remove_fruit/<int:id>/', views.remove_fruit, name='remove_fruit'),

    path('flash_sale/<int:id>/', views.add_to_flash_sale, name='flash_sale'),
    path('flash_sale/', views.flash_sale_fruits, name='flash_sale_fruits'),
    path('regular_sale/<int:id>/', views.make_regular_sale, name='regular_sale'),

    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    
]