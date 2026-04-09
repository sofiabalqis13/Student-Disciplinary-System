# accounts/models.py - Complete models file

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    PROGRAM_CHOICES = [
        ('DCS', 'Diploma in Computer Science'),
        ('DIA', 'Diploma in Accounting'), 
        ('DEC', 'Diploma in English Communication'),
        ('DCD', 'Diploma in Creative Digital Media'),
    ]
    
    SEMESTER_CHOICES = [
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
    ]
    
    # Core student information
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Student ID")
    name = models.CharField(max_length=100, verbose_name="Student Name")
    ic_number = models.CharField(max_length=20, unique=True, verbose_name="IC Number")
    class_name = models.CharField(max_length=50, verbose_name="Class")
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="Semester")
    address = models.TextField(verbose_name="Address")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    program = models.CharField(max_length=3, choices=PROGRAM_CHOICES, verbose_name="Program")
    academic_advisor = models.CharField(max_length=100, verbose_name="Academic Advisor Name")
    
    # Additional fields
   
    def __str__(self):
        return f"{self.name} ({self.student_id})"
    
    def get_total_disciplinary_points(self):
        """Calculate total disciplinary points for resolved cases"""
        return sum(case.get_points() for case in self.disciplinary_cases.filter(status='resolved'))
    
    def has_disciplinary_cases(self):
        """Check if student has any disciplinary cases"""
        return self.disciplinary_cases.exists()
    
    class Meta:
        ordering = ['student_id']
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Supervisor(models.Model):
    """JDK Supervisor model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.admin_id} - {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name = "JDK Supervisor"
        verbose_name_plural = "JDK Supervisors"


class DisciplinaryCase(models.Model):
    """Disciplinary Case model"""
    
    CASE_TYPE_CHOICES = [
        ('attendance', 'Late Attendance'),
        ('dress_code', 'Dress Code Violation'),
        ('smoking', 'Smoking on Campus'),
        ('academic_dishonesty', 'Academic Dishonesty'),
        ('fighting', 'Fighting'),
        ('vandalism', 'Vandalism'),
        ('disrespect', 'Disrespectful Behavior'),
        ('unauthorized_access', 'Unauthorized Access'),
        ('substance_abuse', 'Substance Abuse'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
    ]
    
    # Core case information
    case_id = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='disciplinary_cases')
    case_type = models.CharField(max_length=50, choices=CASE_TYPE_CHOICES)
    description = models.TextField()
    incident_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Case {self.case_id} - {self.student.name}"
    
   
    def case_details(self):
        """Get case details for display"""
        return {
            'type': self.get_case_type_display(),
            'incident_date': self.incident_date,
            'description': self.description,
            'status': self.get_status_display()
        }
    
    def update_status(self, new_status):
        """Update case status"""
        self.status = new_status
        self.save()
    
    class Meta:
        ordering = ['-incident_date']
        verbose_name = "Disciplinary Case"
        verbose_name_plural = "Disciplinary Cases"

class MonthlyReport(models.Model):
    """Monthly Report model"""
    report_id = models.CharField(max_length=20, unique=True)
    month = models.CharField(max_length=20)
    total_cases = models.IntegerField(default=0)
    active_cases = models.IntegerField(default=0)
    resolved_cases = models.IntegerField(default=0)
    
    # Report generation details
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Monthly Report - {self.month} ({self.report_id})"
    
    def generate_report(self, month, year):
        """Generate monthly report automatically"""
        from datetime import datetime
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        cases = DisciplinaryCase.objects.filter(
            incident_date__gte=start_date,
            incident_date__lt=end_date
        )
        
        self.total_cases = cases.count()
        self.active_cases = cases.filter(status__in=['pending', 'under_review']).count()
        self.resolved_cases = cases.filter(status='resolved').count()
        self.save()
        
        return self
    
    class Meta:
        ordering = ['-generated_at']
        verbose_name = "Monthly Report"
        verbose_name_plural = "Monthly Reports"


class StudentLogin(models.Model):
    """Student login tracking model"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    last_login = models.DateTimeField(blank=True, null=True)
    login_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Login for {self.student.name}"
    
    def authenticate_student(self, student_id, ic_number):
        """Authenticate student using ID and IC number"""
        try:
            student = Student.objects.get(
                student_id=student_id,
                ic_number=ic_number
            )
            self.last_login = timezone.now()
            self.login_count += 1
            self.save()
            return True
        except Student.DoesNotExist:
            return False
    
    class Meta:
        verbose_name = "Student Login"
        verbose_name_plural = "Student Logins"





    