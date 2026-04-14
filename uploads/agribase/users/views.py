from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from .models import UserProfile
from order.models import Order


# REGISTER
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # create profile automatically
    UserProfile.objects.create(user=user)

    return Response({"message": "User created"})


# LOGIN
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })


# PROFILE (GET + PATCH)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    # ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    # GET PROFILE
    if request.method == "GET":
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": profile.phone,
            "address": profile.address,
            "state": profile.state,
            "farm_size": profile.farm_size,
            "profile_image": profile.profile_image.url if profile.profile_image else None,
            "date_joined": user.date_joined,
            
            
        })

    # UPDATE PROFILE
    data = request.data

    if 'username' in data and data['username']:
        if User.objects.exclude(pk=user.pk).filter(username=data['username']).exists():
            return Response({"error": "Username already taken"}, status=400)
        user.username = data['username']

    if 'first_name' in data:
        user.first_name = data['first_name']

    if 'last_name' in data:
        user.last_name = data['last_name']

    if 'email' in data:
        user.email = data['email']

    user.save()

    # update extra profile fields
    if 'phone' in data:
        profile.phone = data['phone']

    if 'address' in data:
        profile.address = data['address']

    if 'state' in data:
        profile.state = data['state']

    if 'farm_size' in data:
        profile.farm_size = data['farm_size']

    # profile image upload
    if 'avatar' in request.FILES:
        profile.profile_image = request.FILES['avatar']

    profile.save()

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": profile.phone,
        "address": profile.address,
        "state": profile.state,
        "farm_size": profile.farm_size,
        "profile_image": profile.profile_image.url if profile.profile_image else None,
        "date_joined": user.date_joined,
        
    })


# CHECK EMAIL
@api_view(['POST'])
def check_email(request):
    email = request.data.get('email', '').strip()

    if not email:
        return Response({"error": "Email is required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email found"})

    return Response({"error": "No account found with this email"}, status=404)


# RESET PASSWORD
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email', '').strip()
    new_password = request.data.get('new_password', '')

    if not email or not new_password:
        return Response({"error": "Email and password required"}, status=400)

    if len(new_password) < 6:
        return Response({"error": "Password must be at least 6 characters"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "No account found"}, status=404)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successfully"})