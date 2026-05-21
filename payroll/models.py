from django.db import models
from employees.models import Employee
from django.contrib.auth import get_user_model

# Use the custom User model defined in employees/models.py
User = get_user_model()


class TaxConfig(models.Model):
    """
    Stores Australian income tax brackets for a given financial year.
    Each bracket defines a min/max income range and the applicable tax rate.
    The calculate_tax() service in services.py queries this model to
    determine how much tax to deduct from each employee's gross salary.
    """

    # Financial year label, e.g. '2025-26'
    financial_year = models.CharField(
        max_length=10,
        help_text='e.g. 2025-26'
    )

    # Lower bound of this income bracket (inclusive)
    min_income = models.DecimalField(max_digits=12, decimal_places=2)

    # Upper bound of this income bracket (inclusive)
    max_income = models.DecimalField(max_digits=12, decimal_places=2)

    # Tax rate as a percentage — e.g. 19.00 means 19%
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Percentage e.g. 19.00 means 19%'
    )

    class Meta:
        # Always display brackets in ascending income order
        ordering = ['min_income']

    def __str__(self):
        return (
            f'{self.financial_year}: '
            f'${self.min_income}–${self.max_income} '
            f'@ {self.tax_rate}%'
        )


class PayrollRun(models.Model):
    """
    Represents a single monthly payroll run.
    Each run covers a pay period (pay_start to pay_end) and generates
    individual Payslip records for every active employee.
    The entire run is created atomically — if any payslip fails,
    the whole run is rolled back. See services.run_payroll().
    """

    # Start date of the pay period being processed
    pay_start = models.DateField()

    # End date of the pay period being processed
    pay_end = models.DateField()

    # Date on which employees are paid
    pay_date = models.DateField()

    # Sum of all employees' net pay for this run
    # Populated at the end of the atomic transaction in run_payroll()
    total_amount = models.DecimalField(
        max_digits=14, decimal_places=2, default=0
    )

    # The Payroll Admin user who initiated this run
    # SET_NULL preserves the run record if the admin user is deleted
    processed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    # Automatically set when the run record is first created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show most recent runs first in admin and queries
        ordering = ['-created_at']

    def __str__(self):
        return f'Payroll Run: {self.pay_start} to {self.pay_end}'


class Payslip(models.Model):
    """
    Represents an individual employee payslip for a single payroll run.
    Created automatically by run_payroll() for every active employee
    who has a SalaryStructure. Payslips cascade-delete when their
    parent PayrollRun is deleted, ensuring referential integrity.
    """

    # The payroll run this payslip belongs to
    # CASCADE ensures payslips are deleted when the run is deleted
    payroll_run = models.ForeignKey(
        PayrollRun, on_delete=models.CASCADE,
        related_name='payslips'
    )

    # The employee this payslip is for
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='payslips'
    )

    # Total earnings before any deductions (basic_salary + allowances)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)

    # Income tax deducted based on the applicable TaxConfig bracket
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Additional deductions (e.g. allowances already included in gross)
    deductions = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )

    # Automatically set when the payslip record is created
    generated_at = models.DateTimeField(auto_now_add=True)

    def net_pay(self):
        """
        Calculate take-home pay after tax and deductions.
        Formula: gross_pay - tax_amount - deductions
        """
        return self.gross_pay - self.tax_amount - self.deductions

    def __str__(self):
        return f'Payslip — {self.employee} | {self.payroll_run.pay_date}'
