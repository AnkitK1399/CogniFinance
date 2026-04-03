from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('ANALYST', 'Analyst'),
        ('USER', 'Normal User'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    occupation = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"