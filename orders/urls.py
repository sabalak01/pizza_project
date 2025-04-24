from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('list/', views.order_list, name='order_list'),
    path('change_status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
