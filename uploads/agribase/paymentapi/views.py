from django.shortcuts import render

# Create your views here.
import razorpay
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Order

@api_view(["POST"])
def create_payment(request):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = int(request.data.get("amount")) * 100  # paise

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return Response(payment)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def orders_api(request):

    order = Order.objects.create(
        user=request.user,
        product_id=request.data["product"],
        quantity=request.data["quantity"],
        phone=request.data["phone"],
        email=request.data["email"],
        address=request.data["address"],
        payment_type=request.data["payment_type"]
    )

    return Response({"message": "Order created"})

