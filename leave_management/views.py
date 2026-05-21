from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib import messages
from .models import LeaveType, LeaveBalance, LeaveRequest, ApprovalStep
from .forms import LeaveRequestForm, LeaveTypeForm, LeaveBalanceForm


#Leave Requests

@login_required
def leave_request_list(request):
    requests = LeaveRequest.objects.select_related("employee", "leave_type").order_by("-created_at")
    return render(request, "leave_management/request_list.html", {"requests": requests})


@login_required
def leave_request_create(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect("leave_request_list")
    else:
        form = LeaveRequestForm()
    return render(request, "leave_management/request_form.html", {"form": form})


# Approval logic (the enterprise and atomic-transaction part)

@login_required
@permission_required("leave_management.change_leaverequest", raise_exception=True)
def leave_request_approve(request, pk):
    with transaction.atomic():
        leave = get_object_or_404(
            LeaveRequest.objects.select_for_update(), pk=pk
        )

        if leave.status != "Pending":
            messages.warning(request, "This request has already been processed.")
            return redirect("leave_request_list")

        # Locking the matching balance row so two approvals can't both deduct at once
        balance = LeaveBalance.objects.select_for_update().filter(
            employee=leave.employee, leave_type=leave.leave_type
        ).first()

        days = (leave.end_date - leave.start_date).days + 1

        if balance is None or (balance.total_leave - balance.used_leave) < days:
            messages.error(request, "Not enough leave balance to approve this request.")
            return redirect("leave_request_list")

        balance.used_leave += days
        balance.save()

        leave.status = "Approved"
        leave.save()

        ApprovalStep.objects.create(leave_request=leave, status="accepted")

    messages.success(request, "Leave request approved.")
    return redirect("leave_request_list")


@login_required
@permission_required("leave_management.change_leaverequest", raise_exception=True)
def leave_request_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if leave.status == "Pending":
        leave.status = "Rejected"
        leave.save()
        ApprovalStep.objects.create(leave_request=leave, status="rejected")
        messages.success(request, "Leave request rejected.")
    else:
        messages.warning(request, "This request has already been processed.")
    return redirect("leave_request_list")


# Leave Types ( CRUD) 

@login_required
def leave_type_list(request):
    types = LeaveType.objects.all()
    return render(request, "leave_management/type_list.html", {"types": types})


@login_required
def leave_type_create(request):
    if request.method == "POST":
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave type created.")
            return redirect("leave_type_list")
    else:
        form = LeaveTypeForm()
    return render(request, "leave_management/type_form.html", {"form": form})