from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Course,
    Subject,
    StudentProfile,
    FacultyProfile,
    Question,
    QuestionPaper,
    ActiveQuiz,
    Result,
    PublishedExam,
    CourseConfig,
    Exam,
    ExamQuestion,
    StudentAnswer,
)


# ==================================================
# USER ADMIN
# ==================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "is_student",
        "is_faculty",
        "is_staff",
    )



# ==================================================
# COURSE
# ==================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )



# ==================================================
# SUBJECT
# ==================================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "course",
        "semester",
    )



# ==================================================
# STUDENT PROFILE
# ==================================================

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "name",
        "course",
        "semester",
    )



# ==================================================
# FACULTY PROFILE
# ==================================================

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "name",
    )



# ==================================================
# QUESTION
# ==================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "subject",
        "question_text",
        "marks",
    )



# ==================================================
# QUESTION PAPER
# ==================================================

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "course",
        "semester",
        "duration_minutes",
        "uploaded_at",
    )



# ==================================================
# ACTIVE QUIZ
# ==================================================

@admin.register(ActiveQuiz)
class ActiveQuizAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "course",
        "semester",
        "is_active",
    )



# ==================================================
# RESULT
# ==================================================

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "quiz",
        "score",
        "total_marks",
        "completed_at",
    )



# ==================================================
# PUBLISHED EXAM
# ==================================================

@admin.register(PublishedExam)
class PublishedExamAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "course",
        "semester",
        "exam_date",
    )



# ==================================================
# COURSE CONFIG
# ==================================================

@admin.register(CourseConfig)
class CourseConfigAdmin(admin.ModelAdmin):

    list_display = (
        "course",
        "is_open",
    )



# ==================================================
# EXAM
# ==================================================

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = (
        "exam_name",
        "course",
        "subject",
        "duration",
        "is_published",
    )



# ==================================================
# EXAM QUESTION
# ==================================================

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "exam",
        "question",
    )



# ==================================================
# STUDENT ANSWER
# ==================================================

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "exam",
        "question",
        "selected_answer",
        "is_correct",
        "marks_obtained",
    )