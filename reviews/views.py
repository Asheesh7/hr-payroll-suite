from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from .models import PerformanceReview
from employees.models import Employee
from core.utils import log_action


@login_required
def review_page(request):

    reviews = PerformanceReview.objects.all()

    return render(request, "reviews/review_page.html", {
        "reviews": reviews
    })

@login_required
def create_review(request):

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")

        employee = Employee.objects.get(id=employee_id)

        PerformanceReview.objects.create(
            employee=employee,
            reviewer=request.user,
            rating=rating,
            comments=comments
        )

        log_action(
            request.user,
            f"Created review for employee {employee.id}"
        )

        return redirect("review_page")

    return render(request, "reviews/create_review.html", {
        "employees": employees
    })


@login_required
def update_review(request, pk):

    review = get_object_or_404(
        PerformanceReview,
        pk=pk
    )

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        rating = request.POST.get("rating")
        comments = request.POST.get("comments")

        review.employee = Employee.objects.get(id=employee_id)
        review.rating = rating
        review.comments = comments

        review.save()

        log_action(
            request.user,
            f"Updated review {review.id}"
        )

        return redirect("review_page")

    return render(request, "reviews/update_review.html", {
        "review": review,
        "employees": employees
    })


@login_required
def delete_review(request, pk):

    review = get_object_or_404(
        PerformanceReview,
        pk=pk
    )

    log_action(
        request.user,
        f"Deleted review {review.id}"
    )

    review.delete()

    return redirect("review_page")


@login_required
def top_performers(request):

    top = PerformanceReview.objects.order_by('-rating')[:5]

    log_action(
        request.user,
        "Viewed top performers report"
    )

    return render(request, "reviews/top_performers.html", {
        "top": top
    })


@login_required
def performance_report(request):

    avg_rating = PerformanceReview.objects.aggregate(
        Avg('rating')
    )

    top_employees = PerformanceReview.objects.order_by('-rating')[:10]

    log_action(
        request.user,
        "Viewed performance analytics report"
    )

    return render(request, "reviews/report.html", {
        "avg_rating": avg_rating,
        "top": top_employees
    })

@login_required
def delete_review(request, pk):

    review = get_object_or_404(
        PerformanceReview,
        pk=pk
    )

    if request.method == "POST":

        log_action(
            request.user,
            f"Deleted review {review.id}"
        )

        review.delete()

        return redirect("review_page")

    return render(request, "reviews/delete_review.html", {
        "review": review
    })