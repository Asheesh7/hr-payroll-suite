from django.test import TestCase
from django.urls import reverse
from datetime import date
from employees.models import User, Employee, Department
from .models import LeaveType, LeaveBalance, LeaveRequest, ApprovalStep
from .forms import LeaveRequestForm


class LeaveModelTests(TestCase):
    def setUp(self):
        # Create the supporting data every test needs
        self.user = User.objects.create_user(username="testuser", password="Test@1234")
        self.dept = Department.objects.create(department_name="HR")
        self.employee = Employee.objects.create(
            user=self.user,
            department=self.dept,
            first_name="Test",
            last_name="Person",
            email="test@example.com",
            hire_date=date(2024, 1, 1),
        )
        self.leave_type = LeaveType.objects.create(
            name="Annual Leave", accrual_rate=2.5, is_paid=True
        )
        self.balance = LeaveBalance.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            total_leave=20,
            used_leave=0,
        )

    def test_leave_request_defaults_to_pending(self):
        leave = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 3),
        )
        self.assertEqual(leave.status, "Pending")

    def test_leave_balance_str(self):
        self.assertIn("Annual Leave", str(self.balance))

    def test_leave_type_str(self):
        self.assertEqual(str(self.leave_type), "Annual Leave")


class LeaveFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u2", password="Test@1234")
        self.employee = Employee.objects.create(
            user=self.user, first_name="A", last_name="B",
            email="ab@example.com", hire_date=date(2024, 1, 1),
        )
        self.leave_type = LeaveType.objects.create(name="Sick Leave", accrual_rate=1)

    def test_form_rejects_end_before_start(self):
        form = LeaveRequestForm(data={
            "employee": self.employee.id,
            "leave_type": self.leave_type.id,
            "start_date": "2026-06-10",
            "end_date": "2026-06-05",   # end before start - should be invalid
        })
        self.assertFalse(form.is_valid())

    def test_form_accepts_valid_dates(self):
        form = LeaveRequestForm(data={
            "employee": self.employee.id,
            "leave_type": self.leave_type.id,
            "start_date": "2026-06-05",
            "end_date": "2026-06-10",
        })
        self.assertTrue(form.is_valid())


class LeaveApprovalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="boss", password="Test@1234", email="boss@example.com"
        )
        self.client.login(username="boss", password="Test@1234")
        self.employee = Employee.objects.create(
            user=self.user, first_name="C", last_name="D",
            email="cd@example.com", hire_date=date(2024, 1, 1),
        )
        self.leave_type = LeaveType.objects.create(name="Annual", accrual_rate=2)
        self.balance = LeaveBalance.objects.create(
            employee=self.employee, leave_type=self.leave_type,
            total_leave=20, used_leave=0,
        )
        self.leave = LeaveRequest.objects.create(
            employee=self.employee, leave_type=self.leave_type,
            start_date=date(2026, 6, 1), end_date=date(2026, 6, 3),  # 3 days
        )

    def test_approval_deducts_balance(self):
        self.client.get(reverse("leave_request_approve", args=[self.leave.pk]))
        self.balance.refresh_from_db()
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, "Approved")
        self.assertEqual(float(self.balance.used_leave), 3.0)  # 3 days deducted

    def test_rejection_sets_status(self):
        self.client.get(reverse("leave_request_reject", args=[self.leave.pk]))
        self.leave.refresh_from_db()
        self.assertEqual(self.leave.status, "Rejected")