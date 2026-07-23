
from django import forms

from .models import (
    User,
    FacultyProfile,
    StudentProfile,
    Course,
    Subject,
    Question,
    QuestionPaper,
)

# =========================================
# FACULTY FORM
# =========================================

from django import forms
from .models import User


class FacultyForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    department = forms.CharField(
    max_length=100,
    widget=forms.TextInput(attrs={
        "class": "form-control"
    })
)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
        # =========================================
# STUDENT REGISTRATION FORM
# =========================================

class StudentRegistrationForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = "__all__"
        # =========================================
# COURSE FORM
# =========================================

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"
        # =========================================
# SUBJECT FORM
# =========================================

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = "__all__"
        # =========================================
# QUESTION FORM
# =========================================

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = "__all__"
        # =========================================
# QUESTION PAPER FORM
# =========================================

class QuestionPaperForm(forms.ModelForm):

    class Meta:
        model = QuestionPaper
        fields = "__all__"
        # =========================================
# QUESTION UPLOAD FORM
# =========================================

class QuestionUploadForm(forms.Form):

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="Select Subject"
    )

    excel_file = forms.FileField(
        label="Excel File"
    )