from django.urls import path
from .views import orders_api, my_orders , delete_order,order_count

urlpatterns = [
    path("", my_orders),          # GET /api/orders/
    path("create/", orders_api),  # POST /api/orders/create/
    path("<int:pk>/delete/", delete_order),  # DELETE /api/orders/<pk>/delete/
    path("order-count/", order_count),
]