
# academic/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import create_course, create_assignment, manage_courses, view_assignments, plagiarism_reports, generate_reports

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),  # Add this line
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('', views.home, name='home'),
    
    path('create_course/', views.create_course, name='create_course'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('manage_courses/<int:course_id>/', views.manage_courses, name='manage_courses'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    
    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('view_assignments/', views.view_assignments, name='view_assignments'),
    path('list_assignments/', views.list_assignments, name='list_assignments'),
    path('assignments/edit/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
    path('assignments/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    path('assignments/<int:course_id>/', views.view_assignments, name='view_assignments'),
    
    path('plagiarism_reports/', views.plagiarism_reports, name='plagiarism_reports'),
    
    path('generate_report/<int:assignment_id>/', views.show_assignments, name='generate_report'),
    path('generate_report/<int:assignment_id>/calculate/', views.calculate_plagiarism, name='calculate_plagiarism'),
    
    path('add_students/', views.add_students_to_course, name='add_students'),
    #path('course/<int:course_id>/add_students/', views.add_students_to_course, name='add_students_to_course'),
    path('api/assignments/<int:course_id>/', views.get_assignments_for_course, name='get_assignments_for_course'),

    path('upload-submission/<int:assignment_id>/', views.upload_submission, name='upload_submission'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
