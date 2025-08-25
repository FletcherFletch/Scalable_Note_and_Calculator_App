from django.db import models
from django.conf import settings 
import Helper.billing


# Create your models here.

User = settings.AUTH_USER_MODEL

class Stripe_Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=30)
    init_email = models.EmailField(blank=True, null=True)
   # email= models.CharField(max_length=100)
    stripe_id = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.stripe_id:
            if self.init_email:
                email = self.init_email
                stripe_id = Helper.billing.create_customer(
                    email=email, metadata={
                        "user_id": self.user.id,
                        "username": self.user.username
                    },
                    raw=False
                )
                self.stripe_id = stripe_id
        super().save(*args, **kwargs)

            

    


    
