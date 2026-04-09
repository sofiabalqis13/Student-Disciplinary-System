from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Landing page
    path('', views.landing_page, name='landing_page'),
    
    # Admin URLs
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Student URLs
    path('student-login/', views.student_login_view, name='student_login'),
    path('student-logout/', views.student_logout_view, name='student_logout'),
    path('student-profile/', views.student_profile_view, name='student_profile'),
    path('student-cases/', views.student_cases_view, name='student_cases'),
    
    # General logout (can handle both)
    path('logout/', views.logout_view, name='logout'),
    
    # Student Management
    path('add-student/', views.add_student_view, name='add_student'),
    path('student-list/', views.student_list_view, name='student_list'),
    path('student/<int:student_id>/details/', views.student_details_api, name='student_details'),
    path('student/<int:student_id>/edit/', views.student_edit_view, name='student_edit'),
    path('student/<int:student_id>/delete/', views.student_delete_view, name='student_delete'),
    
    # Disciplinary Cases
    path('disciplinary/cases/', views.disciplinary_cases_view, name='disciplinary_cases'),
    path('disciplinary/case/add/', views.add_disciplinary_case_view, name='add_disciplinary_case'),
    path('disciplinary/case/<int:case_id>/details/', views.disciplinary_case_details_api, name='disciplinary_case_details'),
    path('disciplinary/case/<int:case_id>/edit/', views.edit_disciplinary_case_view, name='edit_disciplinary_case'),
    path('disciplinary/case/<int:case_id>/delete/', views.delete_disciplinary_case_view, name='delete_disciplinary_case'),
    
    # Reports
    path('monthly-report/', views.monthly_report, name='monthly_report'),
    path('download-report/', views.download_report, name='download_report'),
]