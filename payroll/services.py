from decimal import Decimal
from django.db import transaction
from .models import TaxConfig, PayrollRun, Payslip
from employees.models import Employee
import logging

# Module-level logger — writes to logs/hr_payroll.log via LOGGING in settings.py
logger = logging.getLogger(__name__)


def calculate_tax(gross_salary):
    """
    Look up the applicable Australian tax bracket from TaxConfig
    and return the calculated tax amount for the given gross salary.

    Args:
        gross_salary (Decimal): The employee's gross monthly salary.

    Returns:
        Decimal: Tax amount rounded to 2 decimal places.
                 Returns 0.00 if no matching bracket is found.

    Example:
        calculate_tax(Decimal('6500.00'))
        # Matches bracket $45,001–$120,000 @ 32.5%
        # Returns Decimal('2112.50')
    """
    # Query TaxConfig for the bracket that contains this salary
    # Uses lte (less than or equal) and gte (greater than or equal)
    # to find the bracket where min_income <= salary <= max_income
    bracket = TaxConfig.objects.filter(
        min_income__lte=gross_salary,
        max_income__gte=gross_salary
    ).first()

    # No matching bracket — return zero tax (salary below threshold)
    if not bracket:
        return Decimal('0.00')

    # Calculate tax: gross * rate / 100, rounded to 2 decimal places
    tax = (gross_salary * bracket.tax_rate / Decimal('100')).quantize(
        Decimal('0.01')
    )
    return tax


def run_payroll(pay_start, pay_end, pay_date, processed_by):
    """
    Execute the monthly payroll run for all active employees.

    This function is the core enterprise feature of the payroll module.
    It wraps all database writes in a single transaction.atomic() block,
    guaranteeing that either ALL payslips are created and the PayrollRun
    total is updated, or NOTHING is saved if any error occurs mid-run.

    Args:
        pay_start (str|date): Start date of the pay period.
        pay_end   (str|date): End date of the pay period.
        pay_date  (str|date): Date on which employees are paid.
        processed_by (User):  The Payroll Admin initiating the run.

    Returns:
        tuple: (PayrollRun instance, list of Payslip primary keys)

    Raises:
        Exception: Any database error causes a full rollback.
    """
    # Fetch all active employees with their salary structure in one query
    # select_related('salary') avoids N+1 queries in the loop below
    active_employees = Employee.objects.filter(
        status='active'
    ).select_related('salary')

    # Collect payslip IDs to return for Celery task dispatch
    # (Member 5 uses these to queue PDF generation after commit)
    payslip_ids = []

    # Wrap the entire payroll run in an atomic transaction
    # If any operation fails, all changes are rolled back automatically
    with transaction.atomic():

        # Create the parent PayrollRun record first
        # total_amount starts at 0 and is updated at the end of the loop
        payroll_run = PayrollRun.objects.create(
            pay_start=pay_start,
            pay_end=pay_end,
            pay_date=pay_date,
            processed_by=processed_by,
            total_amount=Decimal('0.00')
        )

        # Running total of all employees' net pay for this run
        total = Decimal('0.00')

        # Process each active employee
        for emp in active_employees:

            # Skip employees with no salary structure configured
            # hasattr check avoids a RelatedObjectDoesNotExist exception
            if not hasattr(emp, 'salary'):
                continue

            # Calculate gross pay from SalaryStructure
            # gross = basic_salary + allowances
            gross = emp.salary.gross_salary()

            # Look up the applicable tax bracket and calculate tax
            tax = calculate_tax(gross)

            # Create the individual payslip for this employee
            payslip = Payslip.objects.create(
                payroll_run=payroll_run,
                employee=emp,
                gross_pay=gross,
                tax_amount=tax,
                # Allowances stored as deductions for payslip display
                deductions=emp.salary.allowances
            )

            # Track the payslip ID for post-commit Celery dispatch
            payslip_ids.append(payslip.pk)

            # Add net pay (gross minus tax) to the running total
            total += gross - tax

        # Update the PayrollRun with the final total net pay
        payroll_run.total_amount = total
        payroll_run.save()

        # Write an audit log entry for compliance and traceability
        logger.info(
            'AUDIT | User=%s | Action=RUN_PAYROLL | PayrollRunID=%s | Total=%.2f',
            processed_by.username, payroll_run.pk, float(total)
        )

    # Return outside the transaction block
    # Celery tasks should be dispatched here (after successful commit)
    return payroll_run, payslip_ids
