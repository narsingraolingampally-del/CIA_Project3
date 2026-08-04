
from .models import(
    User,
    Course,
    Subject,
    StudentProfile,
    FacultyProfile,
    Question,
    QuestionPaper,
    Exam,
    Result,
    ExamQuestion,
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

from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = [

            "course",

            "subject",

            "academic_year",

            "semester",

            "question_text",

            "option1",

            "option2",

            "option3",

            "option4",

            "correct_answer",

            "marks",

        ]


        widgets = {

            "course": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),


            "subject": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),


            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Academic Year (Example: 2026-2027)"
                }
            ),


            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Semester"
                }
            ),


            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter Question"
                }
            ),


            "option1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 1"
                }
            ),


            "option2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 2"
                }
            ),


            "option3": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 3"
                }
            ),


            "option4": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 4"
                }
            ),


            "correct_answer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: option1"
                }
            ),


            "marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Marks"
                }
            ),

        }
# QUESTION PAPER FORM
# =========================================

class QuestionPaperForm(forms.ModelForm):

    class Meta:
        model = QuestionPaper

        fields = [
            "course",
            "subject",
            "academic_year",
            "semester",
            "duration_minutes",
            "file",
        ]

        widgets = {

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 2026-2027"
                }
            ),

            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "duration_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "file": forms.FileInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }
        # =========================================
# QUESTION UPLOAD FORM
# =========================================

class QuestionUploadForm(forms.Form):

    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    academic_year = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    semester = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["course"].queryset = Course.objects.all()
        self.fields["subject"].queryset = Subject.objects.all()
# =========================================

class ExamForm(forms.ModelForm):

    class Meta:

        model = Exam

        fields = [
            "exam_name",
            "course",
            "semester",
            "subject",
            "duration",
            "number_of_questions",
            "start_time",
            "end_time",
            "is_published",
        ]

        widgets = {

            "exam_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Exam Name"
                }
            ),

            "course": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "semester": forms.Select(
                choices=[
                    (1, "Semester 1"),
                    (2, "Semester 2"),
                    (3, "Semester 3"),
                    (4, "Semester 4"),
                    (5, "Semester 5"),
                    (6, "Semester 6"),
                    (7, "Semester 7"),
                    (8, "Semester 8"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "number_of_questions": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "start_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),

            "end_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                }
            ),

            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["course"].queryset = Course.objects.all()
        self.fields["subject"].queryset = Subject.objects.all()

class QuestionPaperUploadForm(forms.ModelForm):

    class Meta:
        model = QuestionPaper

        fields = [
            "course",
            "subject",
            "academic_year",
            "semester",
            "file",
        ]

        widgets = {
            "course": forms.Select(
                attrs={"class": "form-select"}
            ),

            "subject": forms.Select(
                attrs={"class": "form-select"}
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 2026-2027",
                }
            ),

            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "file": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".xlsx,.xls",
                }
            ),
        }