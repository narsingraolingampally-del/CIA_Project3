from django import forms

from quiz.models import Course, Subject, FacultyProfile

from .models import (
    FeedbackForm,
    FeedbackQuestion,
    FeedbackAssignment,
)


class FeedbackFormForm(forms.ModelForm):

    class Meta:
        model = FeedbackForm

        fields = [
            "title",
            "description",
            "response_type",
            "academic_year",
            "start_date",
            "end_date",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter feedback form title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter feedback form description",
                }
            ),

            "response_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2026-27",
                }
            ),

            "start_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),

            "end_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_date"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

        self.fields["end_date"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]


class FeedbackQuestionForm(forms.ModelForm):

    class Meta:
        model = FeedbackQuestion

        fields = [
            "question_text",
            "question_type",
            "option1",
            "option2",
            "option3",
            "option4",
            "display_order",
            "is_required",
        ]

        widgets = {
            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter feedback question",
                }
            ),

            "question_type": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_question_type",
                }
            ),

            "option1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 1",
                }
            ),

            "option2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 2",
                }
            ),

            "option3": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 3",
                }
            ),

            "option4": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Option 4",
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                }
            ),

            "is_required": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        question_type = cleaned_data.get(
            "question_type"
        )

        options = [
            cleaned_data.get("option1"),
            cleaned_data.get("option2"),
            cleaned_data.get("option3"),
            cleaned_data.get("option4"),
        ]

        if question_type == "choice":

            if not any(option for option in options):

                raise forms.ValidationError(
                    "At least one option is required for a multiple-choice question."
                )

        if question_type != "choice":

            cleaned_data["option1"] = None
            cleaned_data["option2"] = None
            cleaned_data["option3"] = None
            cleaned_data["option4"] = None

        return cleaned_data


class FeedbackQuestionUploadForm(forms.Form):

    excel_file = forms.FileField(
        label="Excel File",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx,.xls",
            }
        ),
    )

    def clean_excel_file(self):

        file = self.cleaned_data["excel_file"]

        filename = file.name.lower()

        if not filename.endswith(
            (".xlsx", ".xls")
        ):

            raise forms.ValidationError(
                "Please upload an Excel file (.xlsx or .xls)."
            )

        return file


class FeedbackAssignmentForm(forms.ModelForm):

    semester = forms.ChoiceField(
        label="Semester",
        choices=[
            ("", "---------"),
            (1, "Semester 1"),
            (2, "Semester 2"),
            (3, "Semester 3"),
            (4, "Semester 4"),
            (5, "Semester 5"),
            (6, "Semester 6"),
            (7, "Semester 7"),
            (8, "Semester 8"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("name"),
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all().order_by("name"),
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    faculty = forms.ModelChoiceField(
        queryset=FacultyProfile.objects.select_related("user").order_by(
            "user__username"
        ),
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    class Meta:
        model = FeedbackAssignment
        fields = [
            "course",
            "semester",
            "subject",
            "faculty",
            "academic_year",
            "start_date",
            "end_date",
            "is_active",
        ]

        widgets = {
            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 2026-2027",
                }
            ),
            "start_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["start_date"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

        self.fields["end_date"].input_formats = [
            "%Y-%m-%dT%H:%M"
        ]

    def clean(self):
        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")
        faculty = cleaned_data.get("faculty")

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if semester:
            semester = int(semester)
            cleaned_data["semester"] = semester

        if course and semester and subject:
            if (
                subject.course_id != course.id
                or subject.semester != semester
            ):
                self.add_error(
                    "subject",
                    "Selected subject does not belong to the selected course and semester."
                )

        if course and faculty:
            if faculty.course_id != course.id:
                self.add_error(
                    "faculty",
                    "Selected faculty does not belong to the selected course."
                )

        if start_date and end_date:
            if end_date <= start_date:
                self.add_error(
                    "end_date",
                    "End date must be later than start date."
                )

        return cleaned_data