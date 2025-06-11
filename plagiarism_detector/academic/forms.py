# academic/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Course, Assignment, Submission

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True, help_text='Full Name')
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Phone Number')
    is_student = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'onlyOneCheckbox(this)'}))
    is_teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'onlyOneCheckbox(this)'}))

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone_number', 'password1', 'password2', 'is_student', 'is_teacher')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.is_student = self.cleaned_data['is_student']
            user_profile.is_teacher = self.cleaned_data['is_teacher']
            user_profile.save()
        return user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'course_code', 'description', 'start_date', 'end_date', 'instructors', 'department', 'credits', 'prerequisites']

class AssignmentForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=True,
        label="Course",
        help_text=""
    )
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'submission_format', 'max_marks', 'attachments']
        
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['students']
        widgets = {
            'students': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']
