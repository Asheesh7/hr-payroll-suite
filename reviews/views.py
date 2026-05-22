from django.shortcuts import render, redirect
from django.db.models import Avg

from .models import PerformanceReview
from employees.models import Employee
from core.utils import log_action

def review_page(request):
    reviews = PerformanceReview.objects.all()
    employees = Employee.objects.all()

    return render(request, "reviews/review_page.html", {
        "reviews": reviews,
        "employees": employees
    })

def create_review(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")

        employee = Employee.objects.get(id=employee_id)

        review = PerformanceReview.objects.create(
            employee=employee,
            reviewer=request.user,
            rating=rating,
            comments=comments
        )

        log_action(request.user, f"Created review for employee {employee.id}")

        return redirect("review_page")

    return redirect("review_page")

def top_performers(request):
    top = PerformanceReview.objects.order_by('-rating')[:5]

    log_action(request.user, "Viewed top performers report")

    return render(request, "reviews/top_performers.html", {
        "top": top
    })

def performance_report(request):
    avg_rating = PerformanceReview.objects.aggregate(Avg('rating'))

    top_employees = PerformanceReview.objects.order_by('-rating')[:10]

    return render(request, "reviews/report.html", {
        "avg_rating": avg_rating,
        "top": top_employees
    })