from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create default RBAC groups and permissions'

    def handle(self, *args, **kwargs):
        # Employee Group
        employee_group, _ = Group.objects.get_or_create(name='Employee')
        employee_group.permissions.clear()

        # Line Manager Group
        manager_group, _ = Group.objects.get_or_create(name='Line Manager')
        manager_perms = Permission.objects.filter(
            codename__in=['view_employee', 'view_department']
        )
        manager_group.permissions.set(manager_perms)

        # HR Officer Group
        hr_group, _ = Group.objects.get_or_create(name='HR Officer')
        hr_perms = Permission.objects.filter(
            codename__in=[
                'add_employee', 'change_employee', 'view_employee',
                'add_department', 'change_department', 'view_department'
            ]
        )
        hr_group.permissions.set(hr_perms)

        # Payroll Admin Group
        payroll_group, _ = Group.objects.get_or_create(name='Payroll Administrator')
        payroll_perms = Permission.objects.filter(
            codename__in=['view_employee', 'view_department']
        )
        payroll_group.permissions.set(payroll_perms)

        self.stdout.write(self.style.SUCCESS('Groups created successfully!'))