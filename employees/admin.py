from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Employee


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department', 'status')
    list_filter = ('status', 'employment_type', 'department')
    search_fields = ('first_name', 'last_name', 'email')