from django.db import models
from employees.models import Employee


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    accrual_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class LeaveBalance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_balances")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    total_leave = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    used_leave = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"


class LeaveRequest(models.Model):
    STATUS = [("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} ({self.start_date} to {self.end_date})"


class ApprovalStep(models.Model):
    STATUS = [("pending", "pending"), ("accepted", "accepted"), ("rejected", "rejected")]
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, related_name="approval_steps")
    status = models.CharField(max_length=10, choices=STATUS, default="pending")

    def __str__(self):
        return f"Approval for {self.leave_request} - {self.status}"