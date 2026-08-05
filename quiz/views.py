
from .models import StudentProfile, Course
from .forms import StudentRegistrationForm
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
import random
from .models import Course, Subject, Exam, Result
from django.contrib.auth import get_user_model

from django.db.models import Q


from django.db.models import Count
from .models import Exam, Course, Subject, Question, ExamQuestion


from django.http import HttpResponse

from openpyxl import Workbook
from reportlab.lib.pagesizes import landscape, letter

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet


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


from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")   # redirects to /admin-panel/

        messages.error(request, "Invalid Administrator Login")

    return render(request, "admin_panel/login.html")

# =========================================
# FACULTY LOGIN
# =========================================

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def faculty_login(request):

    # Already logged in
    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_faculty:
            return redirect("faculty_dashboard")

        if request.user.is_student:
            return redirect("student_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            messages.error(
                request,
                "Invalid username or password."
            )
            return render(request, "faculty/login.html")

        if not user.is_active:
            messages.error(
                request,
                "Your account is disabled."
            )
            return render(request, "faculty/login.html")

        login(request, user)

        # Redirect back to the page the user originally requested
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)

        # Default redirects
        if user.is_superuser:
            return redirect("admin_dashboard")

        if user.is_faculty:
            return redirect("faculty_dashboard")

        if user.is_student:
            return redirect("student_dashboard")

        messages.error(
            request,
            "You do not have permission to login."
        )
        return redirect("faculty_login")

    return render(
        request,
        "faculty/login.html"
    )
# =========================================
# LOGOUT
# =========================================

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


# ===========================================
# USER ROLE CHECKS
# ===========================================

def is_admin(user):
    return user.is_authenticated and user.is_superuser



def is_student(user):
    return user.is_authenticated and user.is_student


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

    faculty = get_object_or_404(
        FacultyProfile,
        user=request.user
    )


    total_questions = Question.objects.count()


    total_exams = Exam.objects.count()


    total_students = StudentProfile.objects.count()


    total_results = Result.objects.count()



    recent_exams = Exam.objects.select_related(
        "course",
        "subject"
    ).order_by(
        "-id"
    )[:5]



    context = {

        "faculty": faculty,

        "total_questions": total_questions,

        "total_exams": total_exams,

        "total_students": total_students,

        "total_results": total_results,

        "recent_exams": recent_exams,

    }



    return render(

        request,

        "faculty/dashboard.html",

        context

    )


# =========================================
# TAKE QUIZ
# =========================================

# =========================================
# TAKE EXAM
# =========================================

@login_required
@user_passes_test(is_student)
def take_exam(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        is_published=True
    )


    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )


    # Check student belongs to exam course
    if student.course != exam.course:

        messages.error(
            request,
            "You are not allowed to attend this exam."
        )

        return redirect(
            "student_dashboard"
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


    
# =========================================
# VIEW QUESTIONS
# =========================================

@login_required
@user_passes_test(is_faculty)
def view_questions(request):

    questions = Question.objects.all().select_related(
        "course",
        "subject"
    )


    # Filters

    course_id = request.GET.get("course")
    semester = request.GET.get("semester")
    subject_id = request.GET.get("subject")
    search = request.GET.get("search")


    if course_id:

        questions = questions.filter(
            course_id=course_id
        )


    if semester:

        questions = questions.filter(
            semester=semester
        )


    if subject_id:

        questions = questions.filter(
            subject_id=subject_id
        )


    if search:

        questions = questions.filter(
            question_text__icontains=search
        )



    courses = Course.objects.all()

    subjects = Subject.objects.all()



    return render(
        request,
        "faculty/view_questions.html",
        {
            "questions": questions,
            "courses": courses,
            "subjects": subjects,
        }
    )
# =========================================
# VIEW RESULTS
# =========================================
@login_required
@user_passes_test(is_faculty)
def view_results(request):

    results = Result.objects.select_related(
        "student",
        "student__studentprofile",
        "exam",
        "exam__subject",
        "exam__course"
    ).order_by("-completed_at")


    context = {

        "results": results

    }


    return render(
        request,
        "faculty/view_results.html",
        context
    )
# =========================================
# ADMIN DASHBOARD
# =========================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    student_count = StudentProfile.objects.count()
    faculty_count = FacultyProfile.objects.count()
    course_count = Course.objects.count()
    subject_count = Subject.objects.count()
    question_count = Question.objects.count()
    exam_count = Exam.objects.count()
    published_exam_count = Exam.objects.filter(
        is_published=True
    ).count()
    result_count = Result.objects.count()

    recent_exams = Exam.objects.select_related(
        "course",
        "subject"
    ).order_by("-id")[:5]

    # Students by Course
    courses = Course.objects.all()

    course_names = []
    course_students = []

    for course in courses:

        course_names.append(course.name)

        course_students.append(
            StudentProfile.objects.filter(
                course=course
            ).count()
        )

    # Pass / Fail
    pass_count = Result.objects.filter(
        percentage__gte=50
    ).count()

    fail_count = Result.objects.filter(
        percentage__lt=50
    ).count()

    context = {

        "student_count": student_count,
        "faculty_count": faculty_count,
        "course_count": course_count,
        "subject_count": subject_count,
        "question_count": question_count,
        "exam_count": exam_count,
        "published_exam_count": published_exam_count,
        "result_count": result_count,
        "recent_exams": recent_exams,

        "course_names": course_names,
        "course_students": course_students,

        "pass_count": pass_count,
        "fail_count": fail_count,

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

from django.db.models import Q

@login_required
@user_passes_test(is_admin)
def manage_faculty(request):

    search = request.GET.get("search", "")

    faculty = FacultyProfile.objects.select_related(
        "user",
        "course"
    ).prefetch_related(
        "subjects"
    )

    if search:
        faculty = faculty.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )

    faculty = faculty.order_by("user__username")

    return render(
        request,
        "admin_panel/faculty_list.html",
        {
            "faculty": faculty,
            "search": search,
        },
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
# =========================================
# FACULTY CREATE EXAM
# =========================================

@login_required
@user_passes_test(is_faculty)
def create_exam(request):

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            exam = form.save(commit=False)

            # Faculty should create unpublished exam
            exam.is_published = False

            exam.save()


            print("======================")
            print("EXAM CREATED")
            print("ID:", exam.id)
            print("COURSE:", exam.course)
            print("COURSE ID:", exam.course_id)
            print("SUBJECT:", exam.subject)
            print("SUBJECT ID:", exam.subject_id)
            print("======================")


            # Get questions
            questions = Question.objects.filter(
                course_id=exam.course_id,
                subject_id=exam.subject_id
            )


            print(
                "AVAILABLE QUESTIONS:",
                questions.count()
            )


            if questions.count() < exam.number_of_questions:

                messages.error(
                    request,
                    f"Only {questions.count()} questions available."
                )

                exam.delete()

                return redirect(
                    "create_exam"
                )


            # Select random questions

            selected_questions = random.sample(
                list(questions),
                exam.number_of_questions
            )


            # Insert into ExamQuestion table

            for question in selected_questions:

                ExamQuestion.objects.create(
                    exam=exam,
                    question=question
                )


            messages.success(
                request,
                "Exam created successfully."
            )


            return redirect(
                "faculty_dashboard"
            )


        else:

            print(form.errors)


    else:

        form = ExamForm()


    return render(
        request,
        "faculty/create_exam.html",
        {
            "form":form
        }
    )# =========================================
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
@user_passes_test(is_student)
def submit_exam(request):

    if request.method != "POST":
        return redirect("student_dashboard")

    exam = get_object_or_404(
        Exam,
        id=request.POST.get("exam_id")
    )

    # Prevent multiple attempts
    if Result.objects.filter(
        student=request.user,
        exam=exam
    ).exists():

        messages.warning(
            request,
            "You have already attempted this exam."
        )

        return redirect("student_dashboard")

    exam_questions = ExamQuestion.objects.filter(
        exam=exam
    ).select_related("question")

    score = 0
    total_marks = 0

    for eq in exam_questions:

        question = eq.question

        total_marks += question.marks

        selected = request.POST.get(f"q_{question.id}")

        if not selected:
            continue

        option_map = {
            "1": question.option1,
            "2": question.option2,
            "3": question.option3,
            "4": question.option4,
        }

        selected_answer = option_map.get(selected, "").strip().lower()
        correct_answer = str(question.correct_answer).strip().lower()

        print("--------------------------------")
        print("Question :", question.question_text)
        print("Selected :", selected_answer)
        print("Correct  :", correct_answer)

        if selected_answer == correct_answer:
            score += question.marks
            print("✓ Correct")
        else:
            print("✗ Wrong")

    percentage = (
        (score / total_marks) * 100
        if total_marks > 0 else 0
    )

    Result.objects.create(
        student=request.user,
        exam=exam,
        score=score,
        total_marks=total_marks,
        percentage=percentage
    )

    return render(
        request,
        "student/result.html",
        {
            "exam": exam,
            "score": score,
            "total_marks": total_marks,
            "percentage": round(percentage, 2),
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
        course_id = request.POST.get("course")
        semester = request.POST.get("semester")


        if not excel_file:
            messages.error(
                request,
                "Please select an Excel file."
            )
            return redirect("upload_students")


        if not course_id or not semester:
            messages.error(
                request,
                "Please select Course and Semester."
            )
            return redirect("upload_students")


        try:

            course = get_object_or_404(
                Course,
                id=course_id
            )


            df = pd.read_excel(
                excel_file
            )


            # Remove empty rows
            df.dropna(
                how="all",
                inplace=True
            )


            required_columns = [
                "roll_number",
                "aadhaar",
                "name",
                "email"
            ]


            # Validate Excel headers

            for column in required_columns:

                if column not in df.columns:

                    messages.error(
                        request,
                        f"Missing column: {column}"
                    )

                    return redirect(
                        "upload_students"
                    )


            imported = 0
            skipped = 0


            for _, row in df.iterrows():


                # Convert Excel values safely

                roll_number = str(
                    int(row["roll_number"])
                ).strip()


                aadhaar = str(
                    int(row["aadhaar"])
                ).strip()


                name = str(
                    row["name"]
                ).strip()


                email = str(
                    row["email"]
                ).strip()



                # Skip duplicate username

                if User.objects.filter(
                    username=roll_number
                ).exists():

                    skipped += 1
                    continue



                # Create User account

                user = User.objects.create_user(

                    username=roll_number,

                    password=aadhaar,

                    first_name=name,

                    email=email

                )


                # Custom User fields

                user.is_student = True

                # User.course is CharField
                user.course = course.name

                user.semester = int(
                    semester
                )

                user.save()



                # Create Student Profile

                StudentProfile.objects.create(

                    user=user,

                    name=name,

                    course=course,

                    semester=int(
                        semester
                    )

                )


                imported += 1



            messages.success(

                request,

                f"{imported} students uploaded successfully."

            )


            if skipped:

                messages.warning(

                    request,

                    f"{skipped} duplicate students skipped."

                )


            return redirect(
                "manage_students"
            )



        except Exception as e:


            import traceback

            print(
                traceback.format_exc()
            )


            messages.error(

                request,

                f"Upload failed: {str(e)}"

            )


            return redirect(
                "upload_students"
            )



    courses = Course.objects.all()


    return render(

        request,

        "admin_panel/upload_students.html",

        {
            "courses": courses
        }

    
    )# =========================================
# COURSE MANAGEMENT
# =========================================

@login_required
@user_passes_test(is_admin)
def manage_courses(request):

    courses = Course.objects.all().order_by("id")

    context = {
        "courses": courses,
        "total_courses": courses.count(),
    }

    return render(
        request,
        "admin_panel/manage_courses.html",
        context
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

    subjects = Subject.objects.select_related(
        "course"
    ).all().order_by("id")

    context = {

        "subjects": subjects,

        "total_subjects": subjects.count(),

    }

    return render(
        request,
        "admin_panel/manage_subjects.html",
        context
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

from .models import Course, Subject, Question

from django.db.models import Q

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

@login_required
@user_passes_test(is_admin)
def question_bank(request):

    questions = Question.objects.select_related(
        "course",
        "subject"
    ).all().order_by("-id")

    courses = Course.objects.all()
    subjects = Subject.objects.all()

    search = request.GET.get("search")
    course = request.GET.get("course")
    subject = request.GET.get("subject")
    semester = request.GET.get("semester")

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

    context = {
        "questions": questions,
        "courses": courses,
        "subjects": subjects,
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
@user_passes_test(is_faculty)
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


    return redirect(
        "view_questions"
    )
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

            paper = form.save()

            messages.success(
                request,
                "Question paper uploaded successfully"
            )

            return redirect(
                "faculty_dashboard"
            )

    else:

        form = QuestionPaperForm()


    return render(
        request,
        "faculty/question_paper_upload.html",
        {
            "form": form
        }
    )
    
# PUBLISH EXAM
# =========================================

@login_required
@user_passes_test(is_admin)
def publish_exam(request, id):

    exam = get_object_or_404(
        Exam,
        id=id
    )


    exam.is_published = True

    exam.save()


    messages.success(
        request,
        f"{exam.exam_name} published successfully."
    )


    return redirect(
        "manage_exams"
    )

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

# =========================================
# ADMIN REPORTS DASHBOARD
# =========================================

@login_required
@user_passes_test(is_admin)
def admin_reports(request):

    results = Result.objects.select_related(
        "student",
        "student__studentprofile",
        "exam",
        "exam__course",
        "exam__subject"
    ).order_by(
        "-completed_at"
    )


    # =====================================
    # FILTER VALUES
    # =====================================

    course_id = request.GET.get("course")

    subject_id = request.GET.get("subject")

    exam_id = request.GET.get("exam")

    semester = request.GET.get("semester")



    # =====================================
    # APPLY FILTERS
    # =====================================


    if course_id:

        results = results.filter(
            exam__course_id=course_id
        )


    if subject_id:

        results = results.filter(
            exam__subject_id=subject_id
        )


    if exam_id:

        results = results.filter(
            exam_id=exam_id
        )


    if semester:

        results = results.filter(
            student__studentprofile__semester=semester
        )



    # =====================================
    # PASS / FAIL STATUS
    # =====================================

    for result in results:

        if result.percentage >= 40:

            result.status = "PASS"

        else:

            result.status = "FAIL"



    # =====================================
    # STATISTICS
    # =====================================


    total_results = results.count()



    total_students = results.values(
        "student_id"
    ).distinct().count()



    average_percentage = 0


    if total_results:

        average_percentage = round(

            sum(
                float(result.percentage)
                for result in results
            )
            /
            total_results,

            2

        )



    pass_count = results.filter(
        percentage__gte=40
    ).count()



    fail_count = results.filter(
        percentage__lt=40
    ).count()



    highest_score = None


    if total_results:

        highest_score = results.order_by(
            "-percentage"
        ).first()



    # =====================================
    # DROPDOWN DATA
    # =====================================


    courses = Course.objects.all().order_by(
        "name"
    )


    subjects = Subject.objects.all().order_by(
        "name"
    )


    exams = Exam.objects.all().order_by(
        "-id"
    )


    semesters = range(
        1,
        9
    )



    # =====================================
    # CONTEXT
    # =====================================


    context = {

        "results": results,


        # dropdowns

        "courses": courses,

        "subjects": subjects,

        "exams": exams,

        "semesters": semesters,


        # selected filters

        "selected_course": course_id,

        "selected_subject": subject_id,

        "selected_exam": exam_id,

        "selected_semester": semester,


        # statistics

        "total_results": total_results,

        "total_students": total_students,

        "average_percentage": average_percentage,

        "pass_count": pass_count,

        "fail_count": fail_count,

        "highest_score": highest_score,

    }



    return render(

        request,

        "admin_panel/reports.html",

        context

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

            exam = form.save(commit=False)

            exam.created_by = request.user
            exam.is_published = False


            questions = list(
                Question.objects.filter(
                    course=exam.course,
                    subject=exam.subject,
                    semester=exam.semester,
                )
            )


            if len(questions) < exam.number_of_questions:

                messages.error(
                    request,
                    f"Only {len(questions)} questions available for Semester {exam.semester}"
                )

                return redirect(
                    "admin_create_exam"
                )


            exam.save()


            selected_questions = random.sample(
                questions,
                exam.number_of_questions
            )


            for question in selected_questions:

                ExamQuestion.objects.create(
                    exam=exam,
                    question=question
                )


            messages.success(
                request,
                "Exam created successfully"
            )


            return redirect(
                "manage_exams"
            )


    else:

        form = ExamForm()



    exams = Exam.objects.all()


    context = {

        "form": form,

        "total_exams": exams.count(),

        "published_exams": exams.filter(
            is_published=True
        ).count(),

        "draft_exams": exams.filter(
            is_published=False
        ).count(),

        "total_questions": Question.objects.count(),

    }


    return render(
        request,
        "admin_panel/create_exam.html",
        context
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
@login_required
@user_passes_test(is_admin)
def edit_exam(request, id):

    exam = get_object_or_404(
        Exam,
        id=id
    )

    if request.method == "POST":

        form = ExamForm(
            request.POST,
            instance=exam
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam updated successfully."
            )

            return redirect("manage_exams")

    else:

        form = ExamForm(
            instance=exam
        )

    return render(
        request,
        "admin_panel/edit_exam.html",
        {
            "form": form,
            "exam": exam
        }
    )
from django.db.models import Q


from django.db.models import Q
from .models import StudentProfile, Course


from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import StudentProfile, Course


@login_required
@user_passes_test(is_admin)
def manage_students(request):

    students = StudentProfile.objects.select_related(
        "user",
        "course"
    )


    # Search Filter
    search = request.GET.get("search", "")

    if search:

        students = students.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )


    # Course Filter

    course = request.GET.get("course", "")

    if course:

        students = students.filter(
            course__id=course
        )


    # Semester Filter

    semester = request.GET.get("semester", "")

    if semester:

        students = students.filter(
            user__semester=int(semester)
        )


    students = students.order_by("id")


    courses = Course.objects.all()


    return render(
        request,
        "admin_panel/student_list.html",
        {
            "students": students,
            "courses": courses,
            "total_students": students.count()
        }
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def student_dashboard(request):

    # Prevent admin/faculty access
    if not request.user.is_student:
        messages.error(
            request,
            "Only students can access Student Dashboard."
        )

        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_faculty:
            return redirect("faculty_dashboard")

        return redirect("index")

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    exams = Exam.objects.filter(
        course=student.course,
        is_published=True
    )

    results = Result.objects.filter(
        student=request.user
    )

    attempted_exam_ids = results.values_list(
        "exam_id",
        flat=True
    )

    context = {
        "student": student,
        "exams": exams,
        "results": results,
        "attempted_exam_ids": list(attempted_exam_ids),
    }

    return render(
        request,
        "student/dashboard.html",
        context
    )

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index")

@login_required
@user_passes_test(is_admin)
def load_subjects(request):

    course_id = request.GET.get("course")

    subjects = Subject.objects.filter(
        course_id=course_id
    ).values(
        "id",
        "name",
        "semester"
    )

    return JsonResponse(
        list(subjects),
        safe=False
    )
@login_required
@user_passes_test(is_admin)
def view_exam_questions(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    questions = ExamQuestion.objects.filter(
        exam=exam
    ).select_related(
        "question"
    )

    return render(
        request,
        "admin_panel/view_exam_questions.html",
        {
            "exam": exam,
            "questions": questions,
        }
    )
@login_required
@user_passes_test(is_admin)
def export_reports_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        'attachment; filename="CIA_exam_reports.pdf"'
    )


    pdf = SimpleDocTemplate(
        response,
        pagesize=landscape(letter)
    )


    data = [

        [
            "Student",
            "Roll No",
            "Exam",
            "Course",
            "Subject",
            "Score",
            "Total",
            "%"
        ]

    ]



    results = Result.objects.select_related(
        "student",
        "student__studentprofile",
        "exam",
        "exam__course",
        "exam__subject"
    )



    for result in results:


        name = ""


        if hasattr(
            result.student,
            "studentprofile"
        ):

            name = result.student.studentprofile.name



        data.append(

            [

                name,

                result.student.username,

                result.exam.exam_name,

                result.exam.course.name,

                result.exam.subject.name,

                str(result.score),

                str(result.total_marks),

                str(result.percentage)+"%"

            ]

        )



    table = Table(
        data,
        repeatRows=1
    )


    table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),1,None),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE")

            ]

        )

    )


    pdf.build(

        [

            Paragraph(
                "CIA Examination Reports",
                getSampleStyleSheet()["Heading2"]
            ),

            table

        ]

    )


    return response
@login_required
@user_passes_test(is_admin)
def export_reports_excel(request):

    results = Result.objects.select_related(
        "student",
        "student__studentprofile",
        "exam",
        "exam__course",
        "exam__subject"
    )


    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Exam Reports"


    sheet.append(
        [
            "Student Name",
            "Roll Number",
            "Exam",
            "Course",
            "Subject",
            "Score",
            "Total Marks",
            "Percentage",
            "Date"
        ]
    )


    for result in results:


        student_name = ""


        if hasattr(
            result.student,
            "studentprofile"
        ):

            student_name = result.student.studentprofile.name



        sheet.append(
            [

                student_name,

                result.student.username,

                result.exam.exam_name,

                result.exam.course.name,

                result.exam.subject.name,

                result.score,

                result.total_marks,

                f"{result.percentage}%",

                result.completed_at.strftime(
                    "%d-%m-%Y"
                )

            ]
        )


    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response["Content-Disposition"] = (
        'attachment; filename="CIA_exam_reports.xlsx"'
    )


    workbook.save(response)


    return response
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(is_faculty)
def export_results(request):

    results = Result.objects.select_related(
        "student",
        "exam",
        "exam__course",
        "exam__subject"
    )


    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = "Student Results"


    sheet.append([
        "Student",
        "Username",
        "Exam",
        "Course",
        "Subject",
        "Score",
        "Total Marks",
        "Percentage",
        "Status",
        "Date"
    ])


    for result in results:

        status = "PASS" if result.percentage >= 40 else "FAIL"


        sheet.append([

            result.student.studentprofile.name,

            result.student.username,

            result.exam.exam_name,

            result.exam.course.name,

            result.exam.subject.name,

            result.score,

            result.total_marks,

            result.percentage,

            status,

            result.completed_at.strftime("%d-%m-%Y %H:%M")

        ])


    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response["Content-Disposition"] = (
        'attachment; filename="student_results.xlsx"'
    )


    workbook.save(response)


    return response
@login_required
@user_passes_test(is_faculty)
def faculty_edit_question(request, pk):

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

            return redirect("view_questions")

    else:

        form = QuestionForm(
            instance=question
        )

    return render(
        request,
        "faculty/edit_question.html",
        {
            "form": form,
            "question": question,
        }
    )
from django.http import FileResponse
from django.conf import settings
import os


@login_required
@user_passes_test(is_faculty)
def download_question_template(request):
    file_path = os.path.join(
        settings.MEDIA_ROOT,
        "question_template.xlsx"
    )

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename="question_template.xlsx"
    )
@login_required
@user_passes_test(is_admin)
def published_exams(request):

    exams = Exam.objects.filter(
        is_published=True
    ).select_related(
        "course",
        "subject"
    ).order_by("-id")


    return render(
        request,
        "admin_panel/published_exams.html",
        {
            "exams": exams
        }
    )
@login_required
@user_passes_test(is_admin)
def unpublish_exam(request, id):

    exam = get_object_or_404(
        Exam,
        id=id
    )

    exam.is_published = False

    exam.save()


    messages.success(
        request,
        "Exam unpublished successfully."
    )


    return redirect(
        "published_exams"
    )
@login_required
@user_passes_test(lambda u: u.is_student)
def student_upcoming_exams(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )


    exams = Exam.objects.filter(
        course=student.course,
        is_published=True
    )


    return render(
        request,
        "student/upcoming_exams.html",
        {
            "student": student,
            "exams": exams
        }
    )



@login_required
@user_passes_test(lambda u: u.is_student)
def student_results(request):

    results = Result.objects.filter(
        student=request.user
    ).select_related(
        "exam",
        "exam__subject"
    ).order_by(
        "-completed_at"
    )


    return render(
        request,
        "student/result.html",
        {
            "results": results
        }
    )
@login_required
@user_passes_test(is_faculty)
def delete_all_questions(request):

    if request.method == "POST":

        count = Question.objects.count()

        Question.objects.all().delete()

        messages.success(
            request,
            f"{count} questions deleted successfully."
        )

    return redirect("view_questions")
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
            instance=student.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect(
                "manage_students"
            )

    else:

        form = StudentRegistrationForm(
            instance=student.user
        )


    return render(
        request,
        "admin_panel/edit_student.html",
        {
            "form": form,
            "student": student
        }
    )
@login_required
@user_passes_test(is_admin)
def delete_selected_students(request):

    if request.method == "POST":

        student_ids = request.POST.getlist("student_ids")

        if student_ids:

            students = StudentProfile.objects.filter(
                id__in=student_ids
            )

            for student in students:
                student.user.delete()

            messages.success(
                request,
                f"{len(student_ids)} students deleted successfully."
            )

        else:

            messages.warning(
                request,
                "Please select students to delete."
            )


    return redirect("manage_students")


User = get_user_model()



@login_required
@user_passes_test(is_admin)
def upload_students(request):

    courses = Course.objects.all()

    if request.method == "POST":

        course_id = request.POST.get("course")
        semester = request.POST.get("semester")
        academic_year = request.POST.get("academic_year")
        excel_file = request.FILES.get("excel_file")

        if not excel_file:
            messages.error(request, "Please select an Excel file.")
            return redirect("upload_students")

        course = Course.objects.get(id=course_id)

        df = pd.read_excel(excel_file)

        imported = 0
        skipped = 0

        for _, row in df.iterrows():

            username = str(row["Username"]).strip()

            if User.objects.filter(username=username).exists():
                skipped += 1
                continue

            password = str(row["Password"]).strip()

            first_name = str(row["First Name"]).strip()

            last_name = str(row["Last Name"]).strip()

            email = str(row["Email"]).strip()

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_student=True,
                course=course,
                semester=int(semester)
            )

            StudentProfile.objects.create(
                user=user,
                course=course,
                semester=int(semester),
                academic_year=academic_year
            )

            imported += 1

        messages.success(
            request,
            f"{imported} students uploaded successfully. {skipped} skipped."
        )

        return redirect("manage_students")

    return render(
        request,
        "admin_panel/student_upload.html",
        {
            "courses": courses
        }
    )