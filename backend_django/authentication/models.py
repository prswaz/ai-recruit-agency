from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role'] # 'username' field is still required by AbstractUser but we auto-fill it or ignore

    def __str__(self):
        return self.email
