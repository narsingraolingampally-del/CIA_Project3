from django import forms
from .models import QuestionPaper, Subject

from .models import Subject


from django import forms
from .models import (
    User,
    Course,
    FacultyProfile,
    QuestionPaper,
    Subject,
)


# =====================================
# QUIZ SETUP FORM
# =====================================

class QuizSetupForm(forms.Form):

    category = forms.ChoiceField(
        choices=[
            ('', '-- Select Category --'),
            ('UG', 'UG'),
            ('PG', 'PG')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'cat'
        })
    )

    course = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'crs'
        })
    )

    semester = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 9)],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'sem'
        })
    )

    stream = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    num_questions = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "course" in self.data:
            selected = self.data.get("course")
            self.fields["course"].choices = [
                (selected, selected)
            ]

            # =====================================
# STUDENT REGISTRATION FORM
# =====================================

class StudentRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "course",
            "semester"
        ]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "course": forms.TextInput(attrs={"class": "form-control"}),
            "semester": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        user.is_student = True

        if commit:
            user.save()

        return user
    
    # =====================================
# FACULTY REGISTRATION FORM
# =====================================

class FacultyRegistrationForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        user.is_faculty = True

        if commit:

            user.save()

            FacultyProfile.objects.create(
                user=user,
                name=self.cleaned_data["name"]
            )

        return user
class QuestionPaperForm(forms.ModelForm):

    class Meta:
        model = QuestionPaper
        fields = [
            "subject",
            "course",
            "semester",
            "duration_minutes",
            "file",
        ]

        widgets = {
            "subject": forms.Select(attrs={
                "class": "form-control"
            }),

            "course": forms.Select(attrs={
                "class": "form-control"
            }),

            "semester": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),

            "duration_minutes": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),

            "file": forms.FileInput(attrs={
                "class": "form-control"
            }),
        }

# =====================================
# COURSE FORM
# =====================================

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Course Name"
            })
        }
            
            # =====================================
# SUBJECT FORM
# =====================================

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = [
            "code",
            "name",
            "course",
            "semester"
        ]

        widgets = {
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Subject Code"
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Subject Name"
            }),

            "course": forms.Select(attrs={
                "class": "form-control"
            }),

            "semester": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
        }

        from django import forms
from .models import Subject


class QuestionUploadForm(forms.Form):

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="-- Select Subject --",
        widget=forms.Select(
            attrs={
                'class':'form-control'
            }
        )
    )

    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )
    # =====================================
# QUESTION BANK UPLOAD FORM
# =====================================

class QuestionUploadForm(forms.Form):

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        empty_label="-- Select Subject --",
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )


    excel_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx"
            }
        )
    )