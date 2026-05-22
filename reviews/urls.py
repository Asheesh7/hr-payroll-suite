from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_page, name="review_page"),
    path('create/', views.create_review, name="create_review"),
    path('top/', views.top_performers, name="top_performers"),
    path('report/', views.performance_report, name='performance_report'),
]