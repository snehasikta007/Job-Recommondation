from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('basic/', views.basic_details, name='basic_details'),
    path('education/', views.education_details, name='education_details'),
    path('skills/', views.skills_details, name='skills_details'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('resume-analysis/', views.resume_analysis, name='resume_analysis'),
    path('about-user/', views.about_user, name='about_user'),
    path('career-advice/', views.career_advice, name='career_advice'),
    path('find-jobs/', views.find_jobs, name='find_jobs'),
    path('save-job/<int:job_id>/', views.toggle_save_job, name='toggle_save_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('ai-chat/', views.ai_chat_response, name='ai_chat_response'),
    path('applications/', views.applications_tracker, name='applications_tracker'),
    path('update-application-status/<int:app_id>/', views.update_application_status, name='update_application_status'),
]
