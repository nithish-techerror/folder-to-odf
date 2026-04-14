from django.urls import path
from .views import products_api, product_detail, my_products, delete_product

urlpatterns = [
    path("", products_api),              # IT IS CALLING GET all products AND POST add product
    path("my/", my_products),            #  IT IS CALLING GET my products
    path("<int:pk>/", delete_product),   #  IT'S CALLING GET single / DELETE product
    path("detail/<int:pk>/", product_detail),  #  IT IS CALLING  product detail
]