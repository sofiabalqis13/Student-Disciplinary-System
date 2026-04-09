# accounts/forms.py - Forms based on requirements

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Student, DisciplinaryCase, MonthlyReport, CaseComment

class StudentForm(forms.ModelForm):
    """Form for adding/updating student profiles as per requirements"""
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'ic_number', 'class_name', 'semester',
            'address', 'phone_number', 'program', 'academic_advisor',
            'email', 'photo'
        ]
        
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024123456'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'ic_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 123456789012'
            }),
            'class_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., DIT1A'
            }),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Complete address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 01234567890'
            }),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'academic_advisor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Academic Advisor Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@email.com'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        
        labels = {
            'student_id': 'Student ID',
            'name': 'Student Name',
            'ic_number': 'IC Number',
            'class_name': 'Class',
            'semester': 'Semester',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'program': 'Program',
            'academic_advisor': 'Academic Advisor',
            'email': 'Email Address',
            'photo': 'Student Photo',
        }
    
    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        # Validate student ID format if needed
        if len(student_id) < 8:
            raise forms.ValidationError("Student ID must be at least 8 characters long.")
        return student_id
    
    def clean_ic_number(self):
        ic_number = self.cleaned_data['ic_number']
        # Basic IC number validation
        if not ic_number.isdigit() or len(ic_number) != 12:
            raise forms.ValidationError("IC Number must be 12 digits.")
        return ic_number


class DisciplinaryCaseForm(forms.ModelForm):
    """Form for adding/updating disciplinary cases"""
    
    class Meta:
        model = DisciplinaryCase
        fields = [
            'case_id', 'student', 'case_type', 'description', 'incident_date',
            'severity', 'location', 'witnesses', 'evidence_file'
        ]
        
        widgets = {
            'case_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., DC2024001'
            }),
            'student': forms.Select(attrs={
                'class': 'form-control',
                'id': 'student-select'
            }),
            'case_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed description of the incident'
            }),
            'incident_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where the incident occurred'
            }),
            'witnesses': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List of witnesses (if any)'
            }),
            'evidence_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            }),
        }
        
        labels = {
            'case_id': 'Case ID',
            'student': 'Student',
            'case_type': 'Case Type',
            'description': 'Case Description',
            'incident_date': 'Incident Date & Time',
            'severity': 'Severity Level',
            'location': 'Location',
            'witnesses': 'Witnesses',
            'evidence_file': 'Evidence File',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order students by student_id for easier selection
        self.fields['student'].queryset = Student.objects.all().order_by('student_id')
        
        # Generate case ID if not provided
        if not self.instance.pk and not self.initial.get('case_id'):
            import uuid
            from datetime import datetime
            year = datetime.now().year
            random_id = str(uuid.uuid4())[:8].upper()
            self.initial['case_id'] = f"DC{year}{random_id}"


class StudentSearchForm(forms.Form):
    """Form for searching students by ID as per requirements"""
    
    search_query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Student ID, Name, or IC Number',
            'id': 'search-input'
        }),
        label='Search Student'
    )
    
    program_filter = forms.ChoiceField(
        choices=[('', 'All Programs')] + Student.PROGRAM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Program'
    )
    
    semester_filter = forms.ChoiceField(
        choices=[('', 'All Semesters')] + Student.SEMESTER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Semester'
    )


class CaseStatusUpdateForm(forms.ModelForm):
    """Form for updating case status in real time"""
    
    class Meta:
        model = DisciplinaryCase
        fields = ['status']
        
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'updateCaseStatus(this.value)'
            })
        }
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes about this status change...'
        }),
        required=False,
        label='Status Change Notes'
    )


class CaseFilterForm(forms.Form):
    """Form for filtering disciplinary cases by status"""
    
    status_filter = forms.ChoiceField(
        choices=[('', 'All Statuses')] + DisciplinaryCase.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Status'
    )
    
    case_type_filter = forms.ChoiceField(
        choices=[('', 'All Case Types')] + DisciplinaryCase.CASE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Case Type'
    )
    
    severity_filter = forms.ChoiceField(
        choices=[('', 'All Severity Levels')] + DisciplinaryCase.SEVERITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filter by Severity'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )


class StudentLoginForm(forms.Form):
    """Form for student login using ID and IC number"""
    
    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Student ID',
            'autofocus': True
        }),
        label='Student ID'
    )
    
    ic_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your IC Number (12 digits)',
            'pattern': '[0-9]{12}',
            'title': 'Please enter 12 digits'
        }),
        label='IC Number'
    )
    
    def clean_ic_number(self):
        ic_number = self.cleaned_data['ic_number']
        if not ic_number.isdigit() or len(ic_number) != 12:
            raise forms.ValidationError("IC Number must be exactly 12 digits.")
        return ic_number
    
    def authenticate_student(self):
        """Authenticate student using provided credentials"""
        student_id = self.cleaned_data.get('student_id')
        ic_number = self.cleaned_data.get('ic_number')
        
        try:
            student = Student.objects.get(
                student_id=student_id,
                ic_number=ic_number
            )
            return student
        except Student.DoesNotExist:
            raise forms.ValidationError("Invalid Student ID or IC Number.")


class JDKSupervisorLoginForm(AuthenticationForm):
    """Custom login form for JDK Supervisor"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class MonthlyReportForm(forms.ModelForm):
    """Form for generating monthly reports"""
    
    class Meta:
        model = MonthlyReport
        fields = ['month']
        
        widgets = {
            'month': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., January 2024'
            })
        }
    
    report_month = forms.ChoiceField(
        choices=[
            ('1', 'January'), ('2', 'February'), ('3', 'March'),
            ('4', 'April'), ('5', 'May'), ('6', 'June'),
            ('7', 'July'), ('8', 'August'), ('9', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Month'
    )
    
    report_year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '2020',
            'max': '2030',
            'value': '2024'
        }),
        label='Year'
    )


class CaseCommentForm(forms.ModelForm):
    """Form for adding comments to disciplinary cases"""
    
    class Meta:
        model = CaseComment
        fields = ['comment']
        
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your comment here...'
            })
        }
        
        labels = {
            'comment': 'Comment'
        }


class BulkCaseUpdateForm(forms.Form):
    """Form for bulk updating multiple cases"""
    
    selected_cases = forms.CharField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    bulk_action = forms.ChoiceField(
        choices=[
            ('update_status', 'Update Status'),
            ('assign_supervisor', 'Assign Supervisor'),
            ('add_comment', 'Add Comment'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Bulk Action'
    )
    
    new_status = forms.ChoiceField(
        choices=DisciplinaryCase.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='New Status'
    )
    
    bulk_comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Comment to add to selected cases...'
        }),
        label='Bulk Comment'
    )