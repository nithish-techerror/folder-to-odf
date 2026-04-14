from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from product.models import Product


# CREATE ORDER
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def orders_api(request):

    product_id = request.data.get("product")
    quantity = request.data.get("quantity")
    payment_type = request.data.get("payment_type")

    name = request.data.get("name")
    email = request.data.get("email")
    phone = request.data.get("phone")
    address = request.data.get("address")

    try:
        product = Product.objects.get(id=product_id)

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            payment_type=payment_type,
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)


# GET USER ORDERS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):

    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)


# DELETE ORDER
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):

    order = get_object_or_404(Order, id=pk, user=request.user)
    order.delete()

    return Response({"message": "Order deleted"})

#order count
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_count(request):

    count = Order.objects.filter(user=request.user).count()

    return Response({
        "order_count": count
    })