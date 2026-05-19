from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('line_manager', 'Line Manager'),
        ('hr_officer', 'HR Officer'),
        ('payroll_admin', 'Payroll Admin'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
