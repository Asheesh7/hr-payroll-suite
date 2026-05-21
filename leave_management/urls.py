from django.urls import path
from . import views

urlpatterns = [
    # Leave requests
    path("", views.leave_request_list, name="leave_request_list"),
    path("create/", views.leave_request_create, name="leave_request_create"),
    path("<int:pk>/approve/", views.leave_request_approve, name="leave_request_approve"),
    path("<int:pk>/reject/", views.leave_request_reject, name="leave_request_reject"),
    path("<int:pk>/edit/", views.leave_request_edit, name="leave_request_edit"),
    path("<int:pk>/delete/", views.leave_request_delete, name="leave_request_delete"),

    # Leave types
    path("types/", views.leave_type_list, name="leave_type_list"),
    path("types/create/", views.leave_type_create, name="leave_type_create"),
]