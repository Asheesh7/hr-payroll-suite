from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_leave_approval_email(employee_email, employee_name):
    """
    Send email when a leave request is approved.
    """

    subject = "Leave Request Approved"

    message = f"""
Hello {employee_name},

Your leave request has been approved.

Thank you.

HR Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False,
    )

    return f"Leave approval email sent to {employee_email}"


@shared_task
def send_leave_rejection_email(employee_email, employee_name):
    """
    Send email when a leave request is rejected.
    """

    subject = "Leave Request Rejected"

    message = f"""
Hello {employee_name},

Unfortunately, your leave request has been rejected.

Please contact HR for more information.

HR Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False,
    )

    return f"Leave rejection email sent to {employee_email}"


@shared_task
def send_payslip_email(employee_email, employee_name):
    """
    Send email after payroll processing.
    """

    subject = "Payslip Generated"

    message = f"""
Hello {employee_name},

Your monthly payslip has been generated successfully.

Please log in to the HR Payroll System to view it.

HR Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False,
    )

    return f"Payslip email sent to {employee_email}"


@shared_task
def send_performance_review_reminder(employee_email, employee_name):
    """
    Send performance review reminder.
    """

    subject = "Performance Review Reminder"

    message = f"""
Hello {employee_name},

This is a reminder regarding your upcoming performance review.

Please prepare any necessary documents before the review date.

HR Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False,
    )

    return f"Review reminder sent to {employee_email}"


@shared_task
def send_welcome_email(employee_email, employee_name):
    """
    Send welcome email when a new employee is added.
    """

    subject = "Welcome to the Company"

    message = f"""
Hello {employee_name},

Welcome to our organization.

Your employee account has been successfully created.

We wish you success in your new role.

HR Management System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [employee_email],
        fail_silently=False,
    )

    return f"Welcome email sent to {employee_email}"


@shared_task
def system_health_check():
    """
    Simple Celery test task.
    """

    return "Celery is running successfully."