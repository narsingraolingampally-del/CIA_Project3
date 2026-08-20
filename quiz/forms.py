
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
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter faculty name",
            }
        )
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username",
            }
        )
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter first name",
            }
        )
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter last name",
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter email address",
            }
        )
    )

    department = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter department",
            }
        )
    )

    password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        )
    )

    def clean_username(self):

        username = self.cleaned_data["username"].strip()

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                "This username already exists."
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if (
            password
            and confirm_password
            and password != confirm_password
        ):

            self.add_error(
                "confirm_password",
                "Passwords do not match."
            )

        return cleaned_data
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

# =========================================
# QUESTION FORM
# =========================================

# =========================================
# QUESTION FORM
# =========================================

from django import forms

from .models import (
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
# SEMESTER CHOICES
# =========================================

SEMESTER_CHOICES = [
    ("", "---------"),
    (1, "Semester 1"),
    (2, "Semester 2"),
    (3, "Semester 3"),
    (4, "Semester 4"),
    (5, "Semester 5"),
    (6, "Semester 6"),
    (7, "Semester 7"),
    (8, "Semester 8"),
]


# =========================================
# QUESTION FORM
# =========================================

from django import forms

from .models import (
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


SEMESTER_CHOICES = [
    (1, "Semester 1"),
    (2, "Semester 2"),
    (3, "Semester 3"),
    (4, "Semester 4"),
    (5, "Semester 5"),
    (6, "Semester 6"),
    (7, "Semester 7"),
    (8, "Semester 8"),
]


# =========================================
# QUESTION FORM
# =========================================

class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = [
            "course",
            "semester",
            "subject",
            "academic_year",
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
                    "class": "form-select",
                    "id": "id_course"
                }
            ),

            "semester": forms.Select(
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
                attrs={
                    "class": "form-select",
                    "id": "id_semester"
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_subject"
                }
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 2026-2027"
                }
            ),

            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
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

            "correct_answer": forms.Select(
                choices=[
                    ("", "---------"),
                    ("1", "Option 1"),
                    ("2", "Option 2"),
                    ("3", "Option 3"),
                    ("4", "Option 4"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Marks",
                    "min": "1"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Initially no subjects
        self.fields["subject"].queryset = Subject.objects.none()

        # When editing or when form is submitted
        if self.is_bound:

            course_id = self.data.get("course")
            semester = self.data.get("semester")

            if course_id and semester:

                self.fields["subject"].queryset = Subject.objects.filter(
                    course_id=course_id,
                    semester=semester
                ).order_by("code")

        # When editing an existing question
        elif self.instance and self.instance.pk:

            self.fields["subject"].queryset = Subject.objects.filter(
                course=self.instance.course,
                semester=self.instance.semester
            ).order_by("code")

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        if course and semester and subject:

            if subject.course_id != course.id:

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected course."
                )

            if subject.semester != int(semester):

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected semester."
                )

        return cleaned_data
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

# =========================================================
# QUESTION BULK UPLOAD FORM
# =========================================================
# =========================================================
# QUESTION BULK UPLOAD FORM
# =========================================================

from django import forms

from .models import (
    Course,
    Subject,
)


# ============================================================
# QUESTION UPLOAD FORM
# ============================================================

from django import forms

from .models import (
    Course,
    Subject,
)


# =========================================================
# QUESTION EXCEL UPLOAD FORM
# =========================================================

class QuestionUploadForm(forms.Form):

    # =====================================================
    # COURSE
    # =====================================================

    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("name"),
        required=True,
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_course",
            }
        )
    )

    # =====================================================
    # SEMESTER
    # =====================================================

    semester = forms.ChoiceField(
        required=True,
        choices=[
            ("", "---------"),
            ("1", "Semester 1"),
            ("2", "Semester 2"),
            ("3", "Semester 3"),
            ("4", "Semester 4"),
            ("5", "Semester 5"),
            ("6", "Semester 6"),
            ("7", "Semester 7"),
            ("8", "Semester 8"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_semester",
            }
        )
    )

    # =====================================================
    # SUBJECT
    # =====================================================

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=True,
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_subject",
            }
        )
    )

    # =====================================================
    # ACADEMIC YEAR
    # =====================================================

    academic_year = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Example: 2026-2027",
            }
        )
    )

    # =====================================================
    # EXCEL FILE
    # =====================================================

    excel_file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx,.xls",
            }
        )
    )

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        course_id = self.data.get("course")
        semester = self.data.get("semester")

        if course_id and semester:

            try:

                self.fields["subject"].queryset = (
                    Subject.objects
                    .filter(
                        course_id=int(course_id),
                        semester=int(semester)
                    )
                    .order_by("code", "name")
                )

            except (
                ValueError,
                TypeError
            ):

                self.fields["subject"].queryset = (
                    Subject.objects.none()
                )

    # =====================================================
    # VALIDATION
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        if course and semester and subject:

            semester = int(semester)

            # ---------------------------------------------
            # COURSE VALIDATION
            # ---------------------------------------------

            if subject.course_id != course.id:

                self.add_error(
                    "subject",
                    "Selected subject does not belong "
                    "to the selected course."
                )

            # ---------------------------------------------
            # SEMESTER VALIDATION
            # ---------------------------------------------

            if int(subject.semester) != semester:

                self.add_error(
                    "subject",
                    "Selected subject does not belong "
                    "to the selected semester."
                )

        # ---------------------------------------------
        # ACADEMIC YEAR
        # ---------------------------------------------

        academic_year = cleaned_data.get(
            "academic_year"
        )

        if academic_year:

            academic_year = academic_year.strip()

            if not academic_year:

                self.add_error(
                    "academic_year",
                    "Academic year is required."
                )

            cleaned_data["academic_year"] = (
                academic_year
            )

        return cleaned_data

    # =====================================================
    # EXCEL FILE VALIDATION
    # =====================================================

    def clean_excel_file(self):

        excel_file = self.cleaned_data.get(
            "excel_file"
        )

        if not excel_file:
            return excel_file

        filename = excel_file.name.lower()

        if not filename.endswith(
            (".xlsx", ".xls")
        ):

            raise forms.ValidationError(
                "Only Excel files (.xlsx or .xls) "
                "are allowed."
            )

        return excel_file
    # =========================================================
# QUESTION FORM
# =========================================================

class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = [
            "course",
            "semester",
            "subject",
            "academic_year",
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
                    "class": "form-select",
                    "id": "id_course",
                }
            ),

            "semester": forms.Select(
                choices=SEMESTER_CHOICES,
                attrs={
                    "class": "form-select",
                    "id": "id_semester",
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_subject",
                }
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 2026-2027",
                }
            ),

            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Question",
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

            "correct_answer": forms.Select(
                choices=[
                    ("", "---------"),
                    ("1", "Option 1"),
                    ("2", "Option 2"),
                    ("3", "Option 3"),
                    ("4", "Option 4"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),

            "marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Marks",
                    "min": "1",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["subject"].queryset = Subject.objects.none()

        if self.is_bound:

            course_id = self.data.get("course")
            semester = self.data.get("semester")

            if course_id and semester:

                self.fields["subject"].queryset = Subject.objects.filter(
                    course_id=course_id,
                    semester=semester
                ).order_by("code")

        elif self.instance and self.instance.pk:

            if (
                self.instance.course_id
                and self.instance.semester
            ):

                self.fields["subject"].queryset = Subject.objects.filter(
                    course_id=self.instance.course_id,
                    semester=self.instance.semester
                ).order_by("code")

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        if course and semester and subject:

            if subject.course_id != course.id:

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected course."
                )

            if subject.semester != int(semester):

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected semester."
                )

        return cleaned_data


# =========================================================
# QUESTION PAPER FORM
# =========================================================

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

            "course": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                }
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
                    "min": "1",
                    "max": "8",
                }
            ),

            "duration_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),

            "file": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


# =========================================================
# QUESTION BULK UPLOAD FORM
# =========================================================

# =========================================================
# QUESTION BULK UPLOAD FORM
# =========================================================

# =========================================================
# QUESTION BULK UPLOAD FORM
# =========================================================

# =========================================================
# FACULTY QUESTION UPLOAD FORM
# =========================================================

class FacultyUploadForm(forms.Form):

    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("name"),
        required=True,
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_course",
            }
        )
    )

    semester = forms.ChoiceField(
        required=True,
        choices=[
            ("", "---------"),
            ("1", "Semester 1"),
            ("2", "Semester 2"),
            ("3", "Semester 3"),
            ("4", "Semester 4"),
            ("5", "Semester 5"),
            ("6", "Semester 6"),
            ("7", "Semester 7"),
            ("8", "Semester 8"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_semester",
            }
        )
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=True,
        empty_label="---------",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_subject",
            }
        )
    )

    academic_year = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Example: 2026-2027",
            }
        )
    )

    excel_file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx,.xls",
            }
        )
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        course_id = self.data.get("course")
        semester = self.data.get("semester")

        if course_id and semester:

            try:

                self.fields["subject"].queryset = Subject.objects.filter(
                    course_id=int(course_id),
                    semester=int(semester)
                ).order_by("code")

            except (ValueError, TypeError):

                self.fields["subject"].queryset = Subject.objects.none()

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        if course and semester and subject:

            semester = int(semester)

            if subject.course_id != course.id:

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected course."
                )

            if int(subject.semester) != semester:

                raise forms.ValidationError(
                    "Selected subject does not belong to the selected semester."
                )

        return cleaned_data

class ExamForm(forms.ModelForm):

    # =====================================================
    # SEMESTER
    # =====================================================

    semester = forms.ChoiceField(
        choices=SEMESTER_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_exam_semester",
            }
        )
    )

    # =====================================================
    # META
    # =====================================================

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

            # -------------------------------------------------
            # EXAM NAME
            # -------------------------------------------------

            "exam_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter exam name",
                }
            ),

            # -------------------------------------------------
            # COURSE
            # -------------------------------------------------

            "course": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_exam_course",
                }
            ),

            # -------------------------------------------------
            # SUBJECT
            # -------------------------------------------------

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_exam_subject",
                }
            ),

            # -------------------------------------------------
            # DURATION
            # -------------------------------------------------

            "duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Duration in minutes",
                }
            ),

            # -------------------------------------------------
            # NUMBER OF QUESTIONS
            # -------------------------------------------------

            "number_of_questions": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "placeholder": "Number of questions",
                }
            ),

            # -------------------------------------------------
            # START TIME
            # -------------------------------------------------

            "start_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            # -------------------------------------------------
            # END TIME
            # -------------------------------------------------

            "end_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),

            # -------------------------------------------------
            # PUBLISHED
            # -------------------------------------------------

            "is_published": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # IMPORTANT
        # Initially Subject dropdown is empty
        # -------------------------------------------------

        self.fields["subject"].queryset = (
            Subject.objects.none()
        )

        # -------------------------------------------------
        # POST DATA
        # -------------------------------------------------

        if self.is_bound:

            course_id = self.data.get("course")
            semester_value = self.data.get("semester")

            print(
                "ExamForm POST Course:",
                course_id
            )

            print(
                "ExamForm POST Semester:",
                semester_value
            )

            if course_id and semester_value:

                try:

                    semester_value = int(
                        semester_value
                    )

                    subjects = (
                        Subject.objects
                        .filter(
                            course_id=course_id,
                            semester=semester_value
                        )
                        .order_by("code")
                    )

                    self.fields["subject"].queryset = subjects

                    print(
                        "ExamForm Subjects:",
                        list(
                            subjects.values(
                                "id",
                                "code",
                                "name",
                                "semester"
                            )
                        )
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    self.fields["subject"].queryset = (
                        Subject.objects.none()
                    )

        # -------------------------------------------------
        # EDIT EXISTING EXAM
        # -------------------------------------------------

        elif self.instance and self.instance.pk:

            if (
                self.instance.course_id
                and self.instance.semester
            ):

                self.fields["subject"].queryset = (
                    Subject.objects
                    .filter(
                        course_id=self.instance.course_id,
                        semester=self.instance.semester
                    )
                    .order_by("code")
                )

    # =====================================================
    # CLEAN
    # =====================================================

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        # -------------------------------------------------
        # COURSE + SEMESTER + SUBJECT REQUIRED
        # -------------------------------------------------

        if not course:

            return cleaned_data

        if not semester:

            return cleaned_data

        if not subject:

            return cleaned_data

        # -------------------------------------------------
        # CONVERT SEMESTER
        # -------------------------------------------------

        try:

            semester_value = int(semester)

        except (
            ValueError,
            TypeError
        ):

            raise forms.ValidationError(
                "Invalid semester selected."
            )

        # -------------------------------------------------
        # CHECK SUBJECT COURSE
        # -------------------------------------------------

        if subject.course_id != course.id:

            raise forms.ValidationError(
                "Selected subject does not belong "
                "to the selected course."
            )

        # -------------------------------------------------
        # CHECK SUBJECT SEMESTER
        # -------------------------------------------------

        if int(subject.semester) != semester_value:

            raise forms.ValidationError(
                "Selected subject does not belong "
                "to the selected semester."
            )

        return cleaned_data
    # ============================================================
# FACULTY QUESTION EXCEL UPLOAD FORM
# ============================================================


# ============================================================
# FACULTY QUESTION EXCEL UPLOAD FORM
# ============================================================

class FacultyQuestionUploadForm(forms.Form):

    # --------------------------------------------------------
    # COURSE
    # --------------------------------------------------------

    course = forms.ModelChoiceField(
        queryset=Course.objects.all().order_by("name"),
        required=True,
        empty_label="Select Course",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_course",
            }
        ),
    )

    # --------------------------------------------------------
    # SEMESTER
    # --------------------------------------------------------

    semester = forms.ChoiceField(
        required=True,
        choices=[
            ("", "Select Semester"),
            ("1", "Semester 1"),
            ("2", "Semester 2"),
            ("3", "Semester 3"),
            ("4", "Semester 4"),
            ("5", "Semester 5"),
            ("6", "Semester 6"),
            ("7", "Semester 7"),
            ("8", "Semester 8"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_semester",
            }
        ),
    )

    # --------------------------------------------------------
    # SUBJECT
    # --------------------------------------------------------

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        required=True,
        empty_label="Select Subject",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_subject",
            }
        ),
    )

    # --------------------------------------------------------
    # ACADEMIC YEAR
    # --------------------------------------------------------

    academic_year = forms.CharField(
        required=True,
        max_length=20,
        initial="2026-2027",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "2026-2027",
            }
        ),
    )

    # --------------------------------------------------------
    # EXCEL FILE
    # --------------------------------------------------------

    excel_file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ".xlsx,.xls",
            }
        ),
    )

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        course_id = self.data.get("course")
        semester = self.data.get("semester")

        if course_id and semester:

            try:

                self.fields["subject"].queryset = (
                    Subject.objects
                    .filter(
                        course_id=int(course_id),
                        semester=int(semester),
                    )
                    .order_by("code")
                )

            except (ValueError, TypeError):

                self.fields["subject"].queryset = (
                    Subject.objects.none()
                )

    # ========================================================
    # VALIDATION
    # ========================================================

    def clean(self):

        cleaned_data = super().clean()

        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")
        subject = cleaned_data.get("subject")

        if course and semester and subject:

            semester = int(semester)

            if subject.course_id != course.id:

                raise forms.ValidationError(
                    "Selected subject does not belong to "
                    "the selected course."
                )

            if int(subject.semester) != semester:

                raise forms.ValidationError(
                    "Selected subject does not belong to "
                    "the selected semester."
                )

        return cleaned_data

