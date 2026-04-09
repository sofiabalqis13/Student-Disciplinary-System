# accounts/admin.py - Simplified without unused models

from django.contrib import admin
from .models import Student, DisciplinaryCase, MonthlyReport, Supervisor, StudentLogin

# Custom admin for Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'program', 'semester', 'class_name']
    list_filter = ['program', 'semester']
    search_fields = ['student_id', 'name', 'ic_number']
    readonly_fields = []
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'name', 'ic_number')
        }),
        ('Academic Information', {
            'fields': ('program', 'semester', 'class_name', 'academic_advisor')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address')
        }),
    )

# Custom admin for DisciplinaryCase model
@admin.register(DisciplinaryCase)
class DisciplinaryCaseAdmin(admin.ModelAdmin):
    list_display = ['case_id', 'student', 'case_type', 'status', 'incident_date']
    list_filter = ['status', 'case_type', 'incident_date']
    search_fields = ['case_id', 'student__name', 'student__student_id', 'description']
    readonly_fields = ['case_id']
    date_hierarchy = 'incident_date'
    list_per_page = 25
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_id', 'student', 'case_type', 'status')
        }),
        ('Incident Details', {
            'fields': ('incident_date', 'description')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new cases
            import uuid
            obj.case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        super().save_model(request, obj, form, change)

# Custom admin for Supervisor model
@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ['admin_id', 'user', 'get_full_name', 'department']
    search_fields = ['admin_id', 'user__username', 'user__first_name', 'user__last_name', 'user__email']
    list_filter = ['department']
    
    fieldsets = (
        ('Supervisor Information', {
            'fields': ('user', 'admin_id', 'department')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'

# Custom admin for MonthlyReport model
@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'month', 'total_cases', 'active_cases', 'resolved_cases', 'generated_at', 'generated_by']
    list_filter = ['generated_at', 'generated_by']
    search_fields = ['report_id', 'month']
    readonly_fields = ['generated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_id', 'month', 'generated_by')
        }),
        ('Statistics', {
            'fields': ('total_cases', 'active_cases', 'resolved_cases')
        }),
        ('Metadata', {
            'fields': ('generated_at',),
            'classes': ('collapse',)
        }),
    )

# Custom admin for StudentLogin model
@admin.register(StudentLogin)
class StudentLoginAdmin(admin.ModelAdmin):
    list_display = ['student', 'last_login', 'login_count']
    list_filter = ['last_login']
    search_fields = ['student__name', 'student__student_id']
    readonly_fields = ['last_login', 'login_count']

# Customize the admin site header and title
admin.site.site_header = "KPM Indera Mahkota Discipline Management System"
admin.site.site_title = "KPM Indera Mahkota Admin"
admin.site.index_title = "Welcome to KPM Indera Mahkota Discipline Management System"