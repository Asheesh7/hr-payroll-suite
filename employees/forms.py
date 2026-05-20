from django import forms
from .models import User, Employee, Department


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'department', 'manager', 'first_name', 'last_name',
            'email', 'phone', 'dob', 'hire_date', 'employment_type', 'status'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']