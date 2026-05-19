from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('employees/', include('employees.urls')),
    path('leave/', include('leave_management.urls')),
    path('payroll/', include('payroll.urls')),
    path('reviews/', include('reviews.urls')),
]
