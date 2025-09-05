from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class CustomUser(AbstractUser):
    #For Django User

    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    #For Stripe User
    # email = models.CharField(max_length=100)
    # name = models.CharField(max_length=20)
    user_stripe_id = models.CharField(max_length=500, null=True, blank=True)

    USERNAME_FIELD = 'username'



    def __str__(self):
        return self.username

class Notes(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE )

    def __str__(self):
        return self.title
