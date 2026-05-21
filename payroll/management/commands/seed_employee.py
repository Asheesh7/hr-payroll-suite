from django.core.management.base import BaseCommand
from employees.models import Employee, Department, SalaryStructure
from django.contrib.auth import get_user_model
from decimal import Decimal
import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed a test employee with salary'

    def handle(self, *args, **kwargs):
        dept, _ = Department.objects.get_or_create(department_name='Engineering')

        user, created = User.objects.get_or_create(
            username='test.employee@hrpayroll.com',
            defaults={
                'email': 'test.employee@hrpayroll.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'employee',
            }
        )
        if created:
            user.set_password('Test@1234')
            user.save()

        emp, _ = Employee.objects.get_or_create(
            email='test.employee@hrpayroll.com',
            defaults={
                'user': user,
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '0412345678',
                'hire_date': datetime.date(2024, 1, 1),
                'department': dept,
                'status': 'active',
            }
        )

        SalaryStructure.objects.get_or_create(
            employee=emp,
            defaults={
                'basic_salary': Decimal('6000.00'),
                'allowances': Decimal('500.00'),
            }
        )
        self.stdout.write(self.style.SUCCESS(
            f'Employee {emp} created with salary AUD 6500/month'
        ))
