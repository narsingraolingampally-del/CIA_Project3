from django.conf import settings
from django.db import models

from quiz.models import (
    Course,
    Subject,
    FacultyProfile,
    StudentProfile,
)


class FeedbackForm(models.Model):
    """
    Main feedback questionnaire created and controlled by Admin.
    """

    RESPONSE_TYPE_CHOICES = [
        ("faculty", "Faculty Feedback"),
        ("course", "Course Feedback"),
        ("general", "General Feedback"),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True,
        null=True
    )

    response_type = models.CharField(
        max_length=20,
        choices=RESPONSE_TYPE_CHOICES,
        default="faculty"
    )

    academic_year = models.CharField(
        max_length=20
    )

    is_active = models.BooleanField(
        default=False
    )

    start_date = models.DateTimeField(
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_feedback_forms"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FeedbackQuestion(models.Model):
    """
    Questions belonging to a FeedbackForm.
    """

    QUESTION_TYPE_CHOICES = [
        ("rating", "Rating 1-5"),
        ("yes_no", "Yes / No"),
        ("text", "Text"),
        ("choice", "Multiple Choice"),
    ]

    feedback_form = models.ForeignKey(
        FeedbackForm,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default="rating"
    )

    option1 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    option2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    option3 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    option4 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=1
    )

    is_required = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.question_text


class FeedbackAssignment(models.Model):
    """
    Admin assigns a feedback form to a particular
    course, semester, subject and faculty.
    """

    feedback_form = models.ForeignKey(
        FeedbackForm,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="feedback_assignments"
    )

    semester = models.PositiveIntegerField()

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="feedback_assignments"
    )

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE,
        related_name="feedback_assignments"
    )

    academic_year = models.CharField(
        max_length=20
    )

    start_date = models.DateTimeField(
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.feedback_form.title} - "
            f"{self.course} - "
            f"Semester {self.semester} - "
            f"{self.subject} - "
            f"{self.faculty}"
        )


class FeedbackResponse(models.Model):
    """
    One student's submission for one feedback assignment.
    """

    assignment = models.ForeignKey(
        FeedbackAssignment,
        on_delete=models.CASCADE,
        related_name="responses"
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="feedback_responses"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-submitted_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"],
                name="unique_student_feedback_response"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.user.username} - "
            f"{self.assignment}"
        )


class FeedbackAnswer(models.Model):
    """
    Individual answer given by a student.
    """

    response = models.ForeignKey(
        FeedbackResponse,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        FeedbackQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    answer_text = models.TextField(
        blank=True,
        null=True
    )

    selected_option = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["question__display_order", "id"]

        constraints = [
            models.UniqueConstraint(
                fields=["response", "question"],
                name="unique_response_question_answer"
            )
        ]

    def __str__(self):
        return (
            f"{self.response} - "
            f"{self.question}"
        )