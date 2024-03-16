from django.urls import path
from find_trucks import views

urlpatterns = [
    path('', views.home, name='home'), # For rendering the form
    path('result/', views.home, name='result'),  # For processing the form and displaying the result
]