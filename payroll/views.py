from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from .models import PayrollRun, Payslip, TaxConfig
from .services import run_payroll, calculate_tax
from decimal import Decimal, InvalidOperation


def is_payroll_admin(user):
    """Return True if user is a payroll admin or superuser."""
    return (hasattr(user, 'role') and user.role == 'payroll_admin') \
        or user.is_superuser


@login_required
def payroll_dashboard(request):
    """
    Main payroll dashboard showing recent payroll runs
    and current tax bracket configuration.
    Accessible to all authenticated users.
    """
    runs    = PayrollRun.objects.select_related('processed_by').all()[:10]
    configs = TaxConfig.objects.all()
    return render(request, 'payroll/dashboard.html', {
        'runs': runs,
        'configs': configs,
    })


@login_required
@user_passes_test(is_payroll_admin, login_url='/payroll/')
def payroll_run_view(request):
    """
    Process monthly payroll for all active employees.
    Restricted to Payroll Admin role only.
    Uses atomic transaction to ensure all-or-nothing consistency.
    On success, redirects to dashboard with confirmation message.
    """
    if request.method == 'POST':
        pay_start = request.POST.get('pay_start', '').strip()
        pay_end   = request.POST.get('pay_end', '').strip()
        pay_date  = request.POST.get('pay_date', '').strip()

        if not all([pay_start, pay_end, pay_date]):
            messages.error(request, 'All date fields are required.')
            return render(request, 'payroll/run_payroll.html')

        try:
            payroll_run, payslip_ids = run_payroll(
                pay_start=pay_start,
                pay_end=pay_end,
                pay_date=pay_date,
                processed_by=request.user
            )
            messages.success(
                request,
                f'Payroll run completed successfully. '
                f'{len(payslip_ids)} payslip(s) generated.'
            )
            return redirect('payroll-dashboard')
        except Exception as e:
            messages.error(request, f'Payroll run failed: {str(e)}')

    return render(request, 'payroll/run_payroll.html')


@login_required
def payslip_list(request):
    """
    List payslips based on user role.
    Payroll admins and superusers see all payslips.
    Regular employees see only their own payslips.
    """
    user = request.user
    if is_payroll_admin(user):
        payslips = Payslip.objects.select_related(
            'employee', 'employee__user',
            'employee__department', 'payroll_run'
        ).order_by('-generated_at')
    elif hasattr(user, 'employee_profile'):
        payslips = Payslip.objects.filter(
            employee=user.employee_profile
        ).select_related(
            'employee', 'employee__user', 'payroll_run'
        ).order_by('-generated_at')
    else:
        payslips = Payslip.objects.none()

    return render(request, 'payroll/payslip_list.html', {
        'payslips': payslips
    })


@login_required
def payslip_detail(request, pk):
    """
    Display detailed breakdown for a single payslip.
    Shows gross pay, tax deducted, deductions and net pay.
    """
    payslip = get_object_or_404(
        Payslip.objects.select_related(
            'employee', 'employee__user',
            'employee__department', 'payroll_run',
            'payroll_run__processed_by'
        ),
        pk=pk
    )
    return render(request, 'payroll/payslip_detail.html', {
        'payslip': payslip
    })


@login_required
def tax_config_list(request):
    """
    Display all configured tax brackets ordered by min income.
    Payroll admins see Edit and Delete buttons.
    """
    configs = TaxConfig.objects.all()
    return render(request, 'payroll/tax_config.html', {
        'configs': configs,
        'is_admin': is_payroll_admin(request.user),
    })


@login_required
@user_passes_test(is_payroll_admin, login_url='/payroll/')
def tax_config_create(request):
    """
    Create a new tax bracket.
    Restricted to Payroll Admin only.
    Validates that min income is less than max income
    and tax rate is between 0 and 100.
    """
    if request.method == 'POST':
        try:
            financial_year = request.POST['financial_year']
            min_income     = Decimal(request.POST['min_income'])
            max_income     = Decimal(request.POST['max_income'])
            tax_rate       = Decimal(request.POST['tax_rate'])

            if min_income >= max_income:
                messages.error(
                    request, 'Min income must be less than max income.'
                )
                return render(request, 'payroll/tax_config_form.html', {
                    'action': 'Create'
                })

            if tax_rate < 0 or tax_rate > 100:
                messages.error(
                    request, 'Tax rate must be between 0 and 100.'
                )
                return render(request, 'payroll/tax_config_form.html', {
                    'action': 'Create'
                })

            TaxConfig.objects.create(
                financial_year=financial_year,
                min_income=min_income,
                max_income=max_income,
                tax_rate=tax_rate
            )
            messages.success(request, 'Tax bracket created successfully.')
            return redirect('tax-config')

        except (InvalidOperation, KeyError) as e:
            messages.error(request, f'Invalid input: {str(e)}')

    return render(request, 'payroll/tax_config_form.html', {
        'action': 'Create'
    })


@login_required
@user_passes_test(is_payroll_admin, login_url='/payroll/')
def tax_config_update(request, pk):
    """
    Update an existing tax bracket.
    Restricted to Payroll Admin only.
    Pre-fills form with existing values for easy editing.
    """
    config = get_object_or_404(TaxConfig, pk=pk)

    if request.method == 'POST':
        try:
            config.financial_year = request.POST['financial_year']
            config.min_income     = Decimal(request.POST['min_income'])
            config.max_income     = Decimal(request.POST['max_income'])
            config.tax_rate       = Decimal(request.POST['tax_rate'])

            if config.min_income >= config.max_income:
                messages.error(
                    request, 'Min income must be less than max income.'
                )
                return render(request, 'payroll/tax_config_form.html', {
                    'action': 'Update', 'config': config
                })

            if config.tax_rate < 0 or config.tax_rate > 100:
                messages.error(
                    request, 'Tax rate must be between 0 and 100.'
                )
                return render(request, 'payroll/tax_config_form.html', {
                    'action': 'Update', 'config': config
                })

            config.save()
            messages.success(request, 'Tax bracket updated successfully.')
            return redirect('tax-config')

        except (InvalidOperation, KeyError) as e:
            messages.error(request, f'Invalid input: {str(e)}')

    return render(request, 'payroll/tax_config_form.html', {
        'action': 'Update',
        'config': config
    })


@login_required
@user_passes_test(is_payroll_admin, login_url='/payroll/')
def tax_config_delete(request, pk):
    """
    Delete a tax bracket.
    Restricted to Payroll Admin only.
    Requires POST confirmation to prevent accidental deletion.
    """
    config = get_object_or_404(TaxConfig, pk=pk)
    if request.method == 'POST':
        financial_year = config.financial_year
        min_income     = config.min_income
        max_income     = config.max_income
        config.delete()
        messages.warning(
            request,
            f'Tax bracket {financial_year} '
            f'({min_income}–{max_income}) deleted.'
        )
        return redirect('tax-config')
    return render(request, 'payroll/tax_config_confirm_delete.html', {
        'config': config
    })


@login_required
@user_passes_test(is_payroll_admin, login_url='/payroll/')
def payroll_run_delete(request, pk):
    """
    Delete a payroll run and all associated payslips.
    Restricted to Payroll Admin only.
    Uses atomic transaction — all payslips deleted or none.
    """
    payroll_run = get_object_or_404(PayrollRun, pk=pk)
    if request.method == 'POST':
        with transaction.atomic():
            payslip_count = payroll_run.payslips.count()
            payroll_run.delete()
            messages.warning(
                request,
                f'Payroll run deleted along with '
                f'{payslip_count} payslip(s).'
            )
        return redirect('payroll-dashboard')
    return render(request, 'payroll/payroll_run_confirm_delete.html', {
        'run': payroll_run
    })
