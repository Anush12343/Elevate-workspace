from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('employer/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('employer/jobs/new/', views.job_create, name='job_create'),
    path('employer/jobs/random/', views.random_job, name='random_job'),
    path('employer/jobs/<int:job_id>/edit/', views.job_update, name='job_update'),
    path('employer/jobs/<int:job_id>/delete/', views.job_delete, name='job_delete'),
    path('employer/jobs/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('employer/applications/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
]
