from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from paymentapi import views 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/', include('users.urls')),
    path('api/products/', include('product.urls')),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
    path("create-payment/", views.create_payment),
    path("api/orders/", include("order.urls")),
     

   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
