from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Result
import pandas as pd
import random
import string
from .forms import QuestionForm
from .models import Question, Subject
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
    Exam,
    ExamQuestion,
)

from .forms import (
    FacultyForm,
    StudentRegistrationForm,
    CourseForm,
    SubjectForm,
    QuestionPaperForm,
    QuestionUploadForm,
    QuestionForm,
    ExamForm,
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

    print("LOGGED USER:", request.user.username)

    faculty = get_object_or_404(
        FacultyProfile,
        user=request.user
    )

    total_questions = Question.objects.filter(
        course=faculty.course
    ).count()

    total_exams = Exam.objects.filter(
        course=faculty.course
    ).count()

    total_students = StudentProfile.objects.filter(
        course=faculty.course
    ).count()

    total_results = Result.objects.filter(
        exam__course=faculty.course
    ).count()

    context = {
        "faculty": faculty,
        "total_questions": total_questions,
        "total_exams": total_exams,
        "total_students": total_students,
        "total_results": total_results,
    }

    return render(
        request,
        "faculty/dashboard.html",
        context
    )
# =========================================
# STUDENT DASHBOARD
# =========================================

# =========================================
# STUDENT DASHBOARD
# =========================================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import StudentProfile, Exam, Result

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import StudentProfile, Exam, Result


@login_required
def student_dashboard(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    exams = Exam.objects.filter(
        course=student.course,
        is_published=True
    )

    print("=" * 50)
    print("Logged in user :", request.user.username)
    print("Student course :", student.course)
    print("Course ID      :", student.course.id)
    print("Exam Count     :", exams.count())

    for exam in exams:
        print(exam.id, exam.exam_name)

    print("=" * 50)

    results = Result.objects.filter(
        student=request.user
    )

    return render(
        request,
        "student/dashboard.html",
        {
            "student": student,
            "exams": exams,
            "results": results,
        }
    )
# =========================================
# TAKE QUIZ
# =========================================

# =========================================
# TAKE EXAM
# =========================================

@login_required
def take_exam(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        is_published=True
    )


    exam_questions = exam.exam_questions.select_related(
        "question"
    ).all()


    return render(
        request,
        "student/take_exam.html",
        {
            "exam": exam,
            "exam_questions": exam_questions,
            "duration_seconds": exam.duration * 60,
        },
    )


# =========================================
# SUBMIT QUIZ
# =========================================

# =========================================
# SUBMIT EXAM
# =========================================

@login_required
def submit_exam(request):

    if request.method != "POST":
        return redirect("student_dashboard")


    exam = get_object_or_404(
        Exam,
        id=request.POST.get("exam_id"),
        is_published=True
    )


    exam_questions = exam.exam_questions.select_related(
        "question"
    ).all()


    score = 0
    total_marks = 0


    for eq in exam_questions:

        q = eq.question

        total_marks += q.marks


        answer = request.POST.get(
            f"q_{q.id}"
        )


        if answer:

            if answer.strip().lower() == q.correct_answer.strip().lower():

                score += q.marks



    percentage = 0

    if total_marks:

        percentage = round(
            (score / total_marks) * 100,
            2
        )


    result = Result.objects.create(
        student=request.user,
        exam=exam,
        score=score,
        total_marks=total_marks,
    )


    return render(
        request,
        "student/result.html",
        {
            "subject": exam.subject,
            "score": score,
            "total": total_marks,
            "percentage": percentage,
            "result": result,
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

# ==================================================
# ADD QUESTION
# ==================================================

@login_required
@user_passes_test(is_admin)
def add_question(request):

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Question added successfully."
            )

            return redirect("question_bank")


    else:

        form = QuestionForm()


    return render(
        request,
        "admin_panel/add_question.html",
        {
            "form": form
        }
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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import FacultyForm
from .models import User, FacultyProfile


@login_required
@user_passes_test(is_admin)
def add_faculty(request):

    if request.method == "POST":

        form = FacultyForm(request.POST)

        if form.is_valid():

            if form.cleaned_data["password"] != form.cleaned_data["confirm_password"]:
                messages.error(request, "Passwords do not match.")
                return render(
                    request,
                    "admin_panel/add_faculty.html",
                    {"form": form}
                )

            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(request, "Username already exists.")
                return render(
                    request,
                    "admin_panel/add_faculty.html",
                    {"form": form}
                )

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )

            user.is_faculty = True
            user.save()

            FacultyProfile.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                department=form.cleaned_data["department"],
            )

            messages.success(request, "Faculty added successfully.")

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

    faculty = get_object_or_404(FacultyProfile, id=id)
    user = faculty.user

    if request.method == "POST":

        faculty.name = request.POST.get("name")

        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()
        faculty.save()

        messages.success(request, "Faculty updated successfully.")

        return redirect("manage_faculty")

    return render(
        request,
        "admin_panel/edit_faculty.html",
        {
            "faculty": faculty,
            "user": user
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
# CREATE EXAM
# =========================================

@login_required
def create_exam(request):

    if not (request.user.is_faculty or request.user.is_superuser):
        return redirect("faculty_login")


    if request.method == "POST":

        form = ExamForm(request.POST)


        if form.is_valid():

            exam = form.save(commit=False)

            exam.is_published = False

            exam.save()


            # =====================================
            # RANDOM QUESTION SELECTION
            # =====================================

            questions = Question.objects.filter(
                course=exam.course,
                subject=exam.subject
            ).order_by("?")[:exam.number_of_questions]


            # Create ExamQuestion records

            for q in questions:

                ExamQuestion.objects.create(
                    exam=exam,
                    question=q
                )


            messages.success(
                request,
                f"Exam created successfully with {questions.count()} questions."
            )


            return redirect(
                "faculty_dashboard"
            )


    else:

        form = ExamForm()


    return render(
        request,
        "faculty/create_exam.html",
        {
            "form": form
        }
    )
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
@user_passes_test(lambda user: user.is_faculty or user.is_superuser)
def question_bank(request):

    questions = Question.objects.select_related(
        "course",
        "subject"
    ).order_by("-id")


    search = request.GET.get("search")
    course = request.GET.get("course")
    subject = request.GET.get("subject")
    semester = request.GET.get("semester")
    academic_year = request.GET.get("academic_year")


    if search:
        questions = questions.filter(
            question_text__icontains=search
        )


    if course:
        questions = questions.filter(
            course_id=course
        )


    if subject:
        questions = questions.filter(
            subject_id=subject
        )


    if semester:
        questions = questions.filter(
            semester=semester
        )


    if academic_year:
        questions = questions.filter(
            academic_year=academic_year
        )


    context = {
        "questions": questions,
        "courses": Course.objects.all(),
        "subjects": Subject.objects.all(),
    }


    return render(
        request,
        "admin_panel/question_bank.html",
        context
    )
# =========================================
# UPLOAD QUESTIONS
# =========================================

@login_required
@user_passes_test(is_faculty)
def upload_questions(request):

    if request.method == "POST":

        form = QuestionUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            print("FORM IS VALID")

            course = form.cleaned_data["course"]
            subject = form.cleaned_data["subject"]
            academic_year = form.cleaned_data["academic_year"]
            semester = form.cleaned_data["semester"]

            excel_file = request.FILES["excel_file"]

            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():

                Question.objects.create(
                    course=course,
                    subject=subject,
                    academic_year=academic_year,
                    semester=semester,
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
            print("FORM ERRORS:")
            print(form.errors)

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

        faculty = get_object_or_404(
            FacultyProfile,
            user=request.user
        )

        form = QuestionUploadForm(
            request.POST,
            request.FILES,
            faculty=faculty
        )

        if form.is_valid():

            course = form.cleaned_data["course"]
            subject = form.cleaned_data["subject"]
            academic_year = form.cleaned_data["academic_year"]
            semester = form.cleaned_data["semester"]
            excel_file = form.cleaned_data["excel_file"]

            # Save uploaded Excel file information
            question_paper = QuestionPaper.objects.create(
                course=course,
                subject=subject,
                academic_year=academic_year,
                semester=semester,
                duration_minutes=60,
                file=excel_file
            )

            df = pd.read_excel(excel_file)

            imported = 0

            for _, row in df.iterrows():

                Question.objects.create(

                    course=course,

                    subject=subject,

                    academic_year=academic_year,

                    semester=semester,

                    question_text=row["question_text"],

                    option1=row["option1"],

                    option2=row["option2"],

                    option3=row["option3"],

                    option4=row["option4"],

                    correct_answer=str(row["correct_answer"]),

                    marks=int(row["marks"]),

                )

                imported += 1

            messages.success(
                request,
                f"{imported} questions uploaded successfully."
            )

            return redirect("faculty_dashboard")

    else:

        faculty = get_object_or_404(
            FacultyProfile,
            user=request.user
        )

        form = QuestionUploadForm(
            faculty=faculty
        )

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

    results = Result.objects.select_related(
        "student",
        "quiz"
    ).all().order_by("-completed_at")

    return render(
        request,
        "admin_panel/reports.html",
        {
            "results": results
        }
    )
# =========================================
# MANAGE EXAMS
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_exams(request):

    exams = Exam.objects.select_related(
        "course",
        "subject"
    ).order_by("-created_at")

    return render(
        request,
        "admin_panel/manage_exams.html",
        {
            "exams": exams,
        }
    )
@login_required
@user_passes_test(is_admin)
def upload_faculty(request):

    if request.method == "POST":

        excel_file = request.FILES.get("excel_file")

        if not excel_file:

            messages.error(
                request,
                "Please choose an Excel file."
            )

            return redirect("upload_faculty")

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

                user.is_faculty = True
                user.save()

                FacultyProfile.objects.create(
                    user=user,
                    name=str(row["Name"]),
                    department=str(row["Department"])
                )

                imported += 1

            messages.success(
                request,
                f"{imported} faculty imported successfully."
            )

            if skipped:
                messages.warning(
                    request,
                    f"{skipped} duplicate faculty skipped."
                )

            return redirect("manage_faculty")

        except Exception as e:

            messages.error(request, str(e))

    return render(
        request,
        "admin_panel/upload_faculty.html"
    )


@login_required
@user_passes_test(is_faculty)
def password_generator(request):
    return render(
        request,
        "faculty/password_generator.html"
    )
@login_required
@user_passes_test(is_admin)
def admin_create_exam(request):

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam created successfully."
            )

            return redirect("manage_exams")

    else:

        form = ExamForm()

    return render(
        request,
        "admin_panel/create_exam.html",
        {
            "form": form,
        }
    )
@login_required
@user_passes_test(is_faculty)
def faculty_upload_questions(request):

    if request.method == "POST":

        form = QuestionUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            course = form.cleaned_data["course"]
            subject = form.cleaned_data["subject"]
            academic_year = form.cleaned_data["academic_year"]
            semester = form.cleaned_data["semester"]

            excel_file = request.FILES["excel_file"]

            try:

                df = pd.read_excel(excel_file)

                # Remove extra spaces from column names
                df.columns = df.columns.str.strip()

                print("Excel Columns:", df.columns.tolist())

                required_columns = [
                    "question_text",
                    "option1",
                    "option2",
                    "option3",
                    "option4",
                    "correct_answer",
                    "marks",
                ]

                missing = [
                    col for col in required_columns
                    if col not in df.columns
                ]

                if missing:
                    messages.error(
                        request,
                        f"Missing columns in Excel: {', '.join(missing)}"
                    )
                    return render(
                        request,
                        "faculty/upload_questions.html",
                        {"form": form}
                    )

                for _, row in df.iterrows():

                    Question.objects.create(
                        course=course,
                        subject=subject,
                        academic_year=academic_year,
                        semester=semester,
                        question_text=str(row["question_text"]).strip(),
                        option1=str(row["option1"]).strip(),
                        option2=str(row["option2"]).strip(),
                        option3=str(row["option3"]).strip(),
                        option4=str(row["option4"]).strip(),
                        correct_answer=str(row["correct_answer"]).strip(),
                        marks=int(row["marks"]),
                    )

                messages.success(
                    request,
                    "Questions uploaded successfully."
                )

                return redirect("faculty_dashboard")

            except Exception as e:

                print("UPLOAD ERROR:", e)

                messages.error(
                    request,
                    f"Upload failed: {e}"
                )

        else:

            print(form.errors)

    else:

        form = QuestionUploadForm()

    return render(
        request,
        "faculty/upload_questions.html",
        {
            "form": form
        }
    )
@login_required
@user_passes_test(lambda u: u.is_faculty or u.is_superuser)
def faculty_question_bank(request):

    questions = Question.objects.select_related(
        "course",
        "subject"
    ).order_by("-id")

    return render(
        request,
        "faculty/question_bank.html",
        {
            "questions": questions,
            "courses": Course.objects.all(),
            "subjects": Subject.objects.all(),
        }
    )