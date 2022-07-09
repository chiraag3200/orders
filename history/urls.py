from django.urls import path
from . import views


urlpatterns = [
    path('zomato/total_order_amount', views.ZomatoOrderDetailsView.get_orders)
]
