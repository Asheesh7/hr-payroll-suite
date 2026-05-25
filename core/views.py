from django.shortcuts import render
from .models import AuditLog


def audit_report(request):
    logs = AuditLog.objects.all().order_by('-timestamp')[:50]

    return render(request, "core/audit_report.html", {
        "logs": logs
    })