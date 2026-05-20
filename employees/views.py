from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .models import User, Employee, Department
from .forms import EmployeeForm, DepartmentForm


# ─── Authentication Views ───────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('employee_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'employees/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── Dashboard ──────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    return render(request, 'employees/dashboard.html')


# ─── Employee Views ──────────────────────────────────────────────────────────

@login_required
@permission_required('employees.view_employee', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.filter(status='active').select_related('department', 'manager')
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
@permission_required('employees.add_employee', raise_exception=True)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                employee = form.save()
            messages.success(request, 'Employee created successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})


@login_required
@permission_required('employees.view_employee', raise_exception=True)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
@permission_required('employees.change_employee', raise_exception=True)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee'})


@login_required
@permission_required('employees.change_employee', raise_exception=True)
def employee_deactivate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        with transaction.atomic():
            employee.status = 'inactive'
            employee.save()
        messages.success(request, f'{employee.first_name} has been deactivated.')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_deactivate.html', {'employee': employee})


@login_required
def employee_profile(request):
    employee = get_object_or_404(Employee, user=request.user)
    return render(request, 'employees/profile.html', {'employee': employee})


# ─── Department Views ────────────────────────────────────────────────────────

@login_required
@permission_required('employees.view_department', raise_exception=True)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
@permission_required('employees.add_department', raise_exception=True)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Add Department'})


@login_required
@permission_required('employees.change_department', raise_exception=True)
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'employees/department_form.html', {'form': form, 'title': 'Edit Department'})