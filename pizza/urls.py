from django.urls import path
from . import views

urlpatterns = [
    path('', views.pizza_list, name='pizza_list'),
    path('<int:pk>/', views.pizza_detail, name='pizza_detail'),
    path('add/', views.add_pizza_view, name='add_pizza'),
]
