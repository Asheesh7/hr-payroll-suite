from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.payroll_dashboard, name='payroll-dashboard'),

    # Payroll run
    path('run/', views.payroll_run_view, name='payroll-run'),
    path('run/<int:pk>/delete/', views.payroll_run_delete, name='payroll-run-delete'),

    # Payslips
    path('payslips/', views.payslip_list, name='payslip-list'),
    path('payslips/<int:pk>/', views.payslip_detail, name='payslip-detail'),

    # Tax config — full CRUD
    path('tax/', views.tax_config_list, name='tax-config'),
    path('tax/create/', views.tax_config_create, name='tax-config-create'),
    path('tax/<int:pk>/edit/', views.tax_config_update, name='tax-config-update'),
    path('tax/<int:pk>/delete/', views.tax_config_delete, name='tax-config-delete'),
]
