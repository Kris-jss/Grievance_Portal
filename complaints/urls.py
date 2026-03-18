from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('view/<int:complaint_id>/', views.view_complaint, name='view_complaint'),
    path('delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('archive/<int:complaint_id>/', views.archive_complaint, name='archive_complaint'),
]