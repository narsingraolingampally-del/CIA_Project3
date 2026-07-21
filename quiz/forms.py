
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

class FacultyForm(forms.ModelForm):

    class Meta:
        model = FacultyProfile
        fields = "__all__"
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