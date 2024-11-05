# options_trading/urls.py

from django.urls import path
from trading import views

urlpatterns = [
    path('', views.home, name='home'),
    path('options/<str:instrument_name>/<str:side>/', views.option_chain_view, name='option_chain'),
    path('options/calculate/<str:instrument_name>/<str:side>/', views.calculate_margin_and_premium_view, name='calculate_margin_and_premium'),
]
