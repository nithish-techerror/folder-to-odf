from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    farm_size = models.CharField(max_length=50, blank=True)

    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.user.username