from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='index'),
    path('categories/<int:category_id>', views.category, name='category'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('add_item/', views.add_item, name='add_item'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('buy/', views.buy, name='buy'),
    path('search/<str:category_id>', views.category, name='search')
]
