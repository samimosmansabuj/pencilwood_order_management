from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    USER_TYPE = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
        ('Factory Staff', 'Factory Staff'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE, blank=True, null=True)
    email = models.EmailField(("email address"), blank=True, unique=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile-picture/', blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}' if self.first_name else f'{self.username} | {self.email}'
    

