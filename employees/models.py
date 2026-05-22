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
class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class Employee(models.Model):
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    hire_date = models.DateField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, default='full_time')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class SalaryStructure(models.Model):
    employee     = models.OneToOneField(
                       Employee, on_delete=models.CASCADE,
                       related_name='salary'
                   )
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowances   = models.DecimalField(
                       max_digits=12, decimal_places=2, default=0
                   )

    def gross_salary(self):
        return self.basic_salary + self.allowances

    def __str__(self):
        return f'Salary — {self.employee}'
