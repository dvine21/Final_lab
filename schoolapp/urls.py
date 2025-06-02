from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('edit/student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('edit/subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete/student/<int:student_id>/', views.delete_student, name='delete_student'),
    
    path('edit/grade/<int:grade_id>/', views.edit_grade, name='edit_grade'),
    

]
