from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

import pandas as pd
import random
import string

from .models import (
    User,
    StudentProfile,
    FacultyProfile,
    Course,
    Subject,
    Question,
    QuestionPaper,
    ActiveQuiz,
    PublishedExam,
    Result,
)

from .forms import (
    FacultyForm,
    StudentRegistrationForm,
    CourseForm,
    SubjectForm,
    QuestionPaperForm,
    QuestionUploadForm,
    QuestionForm,
)
# =========================================
# HOME PAGE
# =========================================

def index_page(request):
    return render(request, "index.html")


# =========================================
# STUDENT LOGIN
# =========================================

def student_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_student:
            login(request, user)
            return redirect("student_dashboard")

        messages.error(request, "Invalid Student Login")

    return render(request, "student/login.html")


# =========================================
# FACULTY LOGIN
# =========================================

def faculty_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and (user.is_faculty or user.is_superuser):
            login(request, user)
            return redirect("faculty_dashboard")

        messages.error(request, "Invalid Faculty Login")

    return render(request, "faculty/login.html")


# =========================================
# LOGOUT
# =========================================

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


# =========================================
# PERMISSIONS
# =========================================

def is_admin(user):
    return user.is_staff or user.is_superuser


def is_faculty(user):
    return user.is_authenticated and (
        user.is_faculty or user.is_superuser
    )

# =========================================
# FACULTY DASHBOARD
# =========================================

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):

    papers = QuestionPaper.objects.all().order_by("-id")

    published = PublishedExam.objects.all().order_by("-id")

    return render(
        request,
        "faculty/dashboard.html",
        {
            "papers": papers,
            "published": published,
        },
    )


# =========================================
# STUDENT DASHBOARD
# =========================================

@login_required
def student_dashboard(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    quizzes = ActiveQuiz.objects.filter(
        course=student.course,
        semester=student.semester,
        is_active=True
    )

    results = Result.objects.filter(
        student=request.user
    ).order_by("-completed_at")

    return render(
        request,
        "student/dashboard.html",
        {
            "student": student,
            "quizzes": quizzes,
            "results": results,
        },
    )


# =========================================
# TAKE QUIZ
# =========================================

@login_required
def take_quiz(request, exam_id):

    quiz = get_object_or_404(
        ActiveQuiz,
        id=exam_id
    )

    questions = Question.objects.filter(
        subject=quiz.subject
    )

    return render(
        request,
        "student/take_quiz.html",
        {
            "quiz": quiz,
            "questions": questions,
            "duration_seconds": quiz.duration_minutes * 60,
        },
    )


# =========================================
# SUBMIT QUIZ
# =========================================

@login_required
def submit_quiz(request):

    if request.method != "POST":
        return redirect("student_dashboard")

    quiz = get_object_or_404(
        ActiveQuiz,
        id=request.POST.get("quiz_id")
    )

    questions = Question.objects.filter(
        subject=quiz.subject
    )

    score = 0
    total_marks = 0

    for q in questions:

        total_marks += q.marks

        answer = request.POST.get(f"q_{q.id}")

        if answer:

            selected_option = getattr(q, f"option{answer}")

            if selected_option == q.correct_answer:
                score += q.marks

    percentage = 0

    if total_marks:
        percentage = round((score / total_marks) * 100, 2)

    Result.objects.create(
        student=request.user,
        quiz=quiz,
        score=score,
        total_marks=total_marks,
    )

    return render(
        request,
        "student/result.html",
        {
            "subject": quiz.subject,
            "score": score,
            "total": total_marks,
            "percentage": percentage,
        },
    )


# =========================================
# VIEW QUESTIONS
# =========================================

@login_required
@user_passes_test(is_faculty)
def view_questions(request):

    questions = Question.objects.select_related(
        "subject"
    ).all()

    return render(
        request,
        "faculty/view_questions.html",
        {
            "questions": questions
        },
    )


# =========================================
# VIEW RESULTS
# =========================================

@login_required
@user_passes_test(is_faculty)
def view_results(request):

    results = Result.objects.select_related(
        "student",
        "quiz"
    ).order_by("-completed_at")

    return render(
        request,
        "faculty/view_results.html",
        {
            "results": results
        },
    )
# =========================================
# ADMIN DASHBOARD
# =========================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    context = {

        "student_count": User.objects.filter(
            is_student=True
        ).count(),

        "faculty_count": User.objects.filter(
            is_faculty=True
        ).count(),

        "course_count": Course.objects.count(),

        "subject_count": Subject.objects.count(),

        "question_count": Question.objects.count(),

        "active_exam_count": ActiveQuiz.objects.filter(
            is_active=True
        ).count(),

        "result_count": Result.objects.count(),

    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context
    )


# =========================================
# FACULTY MANAGEMENT
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_faculty(request):

    faculty = FacultyProfile.objects.select_related(
        "user"
    ).all().order_by("user__username")

    return render(
        request,
        "admin_panel/faculty_list.html",
        {
            "faculty": faculty
        }
    )


# =========================================
# ADD FACULTY
# =========================================

@login_required
@user_passes_test(is_admin)
def add_faculty(request):

    if request.method == "POST":

        form = FacultyForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Faculty added successfully."
            )

            return redirect("manage_faculty")

    else:

        form = FacultyForm()

    return render(
        request,
        "admin_panel/add_faculty.html",
        {
            "form": form
        }
    )


# =========================================
# EDIT FACULTY
# =========================================

@login_required
@user_passes_test(is_admin)
def edit_faculty(request, id):

    faculty = get_object_or_404(
        FacultyProfile,
        id=id
    )

    if request.method == "POST":

        form = FacultyForm(
            request.POST,
            instance=faculty
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Faculty updated successfully."
            )

            return redirect("manage_faculty")

    else:

        form = FacultyForm(instance=faculty)

    return render(
        request,
        "admin_panel/edit_faculty.html",
        {
            "form": form
        }
    )


# =========================================
# DELETE FACULTY
# =========================================

@login_required
@user_passes_test(is_admin)
def delete_faculty(request, id):

    faculty = get_object_or_404(
        FacultyProfile,
        id=id
    )

    faculty.user.delete()

    messages.success(
        request,
        "Faculty deleted successfully."
    )

    return redirect("manage_faculty")
# =========================================
# STUDENT MANAGEMENT
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_students(request):

    students = StudentProfile.objects.select_related(
        "user"
    ).all().order_by("user__username")

    return render(
        request,
        "admin_panel/student_list.html",
        {
            "students": students
        }
    )


# =========================================
# ADD STUDENT
# =========================================

@login_required
@user_passes_test(is_admin)
def add_student(request):

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student added successfully."
            )

            return redirect("manage_students")

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "admin_panel/add_student.html",
        {
            "form": form
        }
    )


# =========================================
# EDIT STUDENT
# =========================================

@login_required
@user_passes_test(is_admin)
def edit_student(request, id):

    student = get_object_or_404(
        StudentProfile,
        id=id
    )

    if request.method == "POST":

        form = StudentRegistrationForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("manage_students")

    else:

        form = StudentRegistrationForm(
            instance=student
        )

    return render(
        request,
        "admin_panel/add_student.html",
        {
            "form": form
        }
    )


# =========================================
# DELETE STUDENT
# =========================================

@login_required
@user_passes_test(is_admin)
def delete_student(request, id):

    student = get_object_or_404(
        StudentProfile,
        id=id
    )

    student.user.delete()

    messages.success(
        request,
        "Student deleted successfully."
    )

    return redirect("manage_students")


# =========================================
# UPLOAD STUDENTS
# =========================================

@login_required
@user_passes_test(is_admin)
def upload_students(request):

    if request.method == "POST":

        excel_file = request.FILES.get("excel_file")

        if not excel_file:

            messages.error(
                request,
                "Please choose an Excel file."
            )

            return redirect("upload_students")

        try:

            df = pd.read_excel(excel_file)

            imported = 0
            skipped = 0

            for _, row in df.iterrows():

                username = str(row["Username"]).strip()

                if User.objects.filter(username=username).exists():
                    skipped += 1
                    continue

                user = User.objects.create_user(
                    username=username,
                    password=str(row["Password"]),
                    first_name=str(row["First Name"]),
                    last_name=str(row["Last Name"]),
                    email=str(row["Email"]),
                )

                user.is_student = True
                user.save()

                StudentProfile.objects.create(
                    user=user,
                    course=row["Course"],
                    semester=int(row["Semester"])
                )

                imported += 1

            messages.success(
                request,
                f"{imported} students imported successfully."
            )

            if skipped:
                messages.warning(
                    request,
                    f"{skipped} duplicate students skipped."
                )

            return redirect("manage_students")

        except Exception as e:

            messages.error(request, str(e))

    return render(
        request,
        "admin_panel/upload_students.html"
    )
# =========================================
# COURSE MANAGEMENT
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_courses(request):

    courses = Course.objects.all().order_by("name")

    return render(
        request,
        "admin_panel/course_list.html",
        {
            "courses": courses
        }
    )


@login_required
@user_passes_test(is_admin)
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course added successfully."
            )

            return redirect("manage_courses")

    else:

        form = CourseForm()

    return render(
        request,
        "admin_panel/add_course.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_admin)
def edit_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect("manage_courses")

    else:

        form = CourseForm(instance=course)

    return render(
        request,
        "admin_panel/add_course.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_admin)
def delete_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    course.delete()

    messages.success(
        request,
        "Course deleted successfully."
    )

    return redirect("manage_courses")


# =========================================
# SUBJECT MANAGEMENT
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_subjects(request):

    subjects = Subject.objects.all().order_by(
        "course",
        "semester",
        "name"
    )

    return render(
        request,
        "admin_panel/subject_list.html",
        {
            "subjects": subjects
        }
    )


@login_required
@user_passes_test(is_admin)
def add_subject(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject added successfully."
            )

            return redirect("manage_subjects")

    else:

        form = SubjectForm()

    return render(
        request,
        "admin_panel/add_subject.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_admin)
def edit_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject updated successfully."
            )

            return redirect("manage_subjects")

    else:

        form = SubjectForm(instance=subject)

    return render(
        request,
        "admin_panel/add_subject.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_admin)
def delete_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id
    )

    subject.delete()

    messages.success(
        request,
        "Subject deleted successfully."
    )

    return redirect("manage_subjects")
# =========================================
# QUESTION BANK
# =========================================

@login_required
@user_passes_test(is_admin)
def question_bank(request):

    questions = Question.objects.select_related(
        "subject"
    ).all().order_by("-id")

    return render(
        request,
        "admin_panel/question_bank.html",
        {
            "questions": questions
        }
    )


# =========================================
# UPLOAD QUESTIONS
# =========================================

@login_required
@user_passes_test(is_admin)
def upload_questions(request):

    if request.method == "POST":

        form = QuestionUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            subject = form.cleaned_data["subject"]
            excel_file = request.FILES["excel_file"]

            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():

                Question.objects.create(
                    subject=subject,
                    question_text=row["question_text"],
                    option1=row["option1"],
                    option2=row["option2"],
                    option3=row["option3"],
                    option4=row["option4"],
                    correct_answer=row["correct_answer"],
                    marks=row["marks"],
                )

            messages.success(
                request,
                "Questions uploaded successfully."
            )

            return redirect("question_bank")

    else:

        form = QuestionUploadForm()

    return render(
        request,
        "admin_panel/upload_questions.html",
        {
            "form": form
        }
    )


# =========================================
# EDIT QUESTION
# =========================================

@login_required
@user_passes_test(is_admin)
def edit_question(request, pk):

    question = get_object_or_404(
        Question,
        pk=pk
    )

    if request.method == "POST":

        form = QuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Question updated successfully."
            )

            return redirect("question_bank")

    else:

        form = QuestionForm(instance=question)

    return render(
        request,
        "admin_panel/edit_question.html",
        {
            "form": form
        }
    )


# =========================================
# DELETE QUESTION
# =========================================

@login_required
@user_passes_test(is_admin)
def delete_question(request, pk):

    question = get_object_or_404(
        Question,
        pk=pk
    )

    question.delete()

    messages.success(
        request,
        "Question deleted successfully."
    )

    return redirect("question_bank")


# =========================================
# UPLOAD QUESTION PAPER
# =========================================

@login_required
@user_passes_test(is_faculty)
def upload_question_paper(request):

    if request.method == "POST":

        form = QuestionPaperForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Question Paper uploaded successfully."
            )

            return redirect("faculty_dashboard")

    else:

        form = QuestionPaperForm()

    return render(
        request,
        "faculty/upload_questions.html",
        {
            "form": form
        }
    )


# =========================================
# PUBLISH EXAM
# =========================================

@login_required
@user_passes_test(is_faculty)
def publish_exam(request, id):

    paper = get_object_or_404(
        QuestionPaper,
        id=id
    )

    messages.success(
        request,
        f"{paper.subject} published successfully."
    )

    return redirect("faculty_dashboard")


# =========================================
# DELETE QUESTION PAPER
# =========================================

@login_required
@user_passes_test(is_faculty)
def delete_paper(request, pk):

    paper = get_object_or_404(
        QuestionPaper,
        pk=pk
    )

    paper.delete()

    messages.success(
        request,
        "Question Paper deleted successfully."
    )

    return redirect("faculty_dashboard")
@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    return render(request, "admin_panel/reports.html")

# =========================================
# MANAGE EXAMS
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_exams(request):

    exams = PublishedExam.objects.all().order_by("-id")

    return render(
        request,
        "admin_panel/manage_exams.html",
        {
            "exams": exams,
        }
    )