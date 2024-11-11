from django.urls import path
from .views import *


urlpatterns = [
     path('', index_views, name='index'),
     path('order_menu/<int:food_id>/', order_menu, name='order_menu'),  
     path('checkout/<int:order_id>/', checkout, name='checkout'),  
]
