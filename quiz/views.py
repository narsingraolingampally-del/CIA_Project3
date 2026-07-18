from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import get_object_or_404


from .models import User, FacultyProfile
from .models import Question

import pandas as pd
from django.shortcuts import render, redirect


from .forms import QuestionUploadForm
from .models import Question

import pandas as pd




import traceback
from .models import (
    User,
    Course,
    Subject,
    QuestionPaper,
    Question,
    PublishedExam,
    ActiveQuiz,
    Result,
    StudentProfile,
)

from .forms import (
    QuestionPaperForm,
    StudentRegistrationForm,
    FacultyRegistrationForm,
    CourseForm,
    SubjectForm,
)



# =========================================
# HOME PAGE
# =========================================

def index_page(request):

    return render(
        request,
        "index.html"
    )



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


        if user is None:

            messages.error(
                request,
                "Invalid username or password"
            )

            return render(
                request,
                "student/login.html"
            )


        if not user.is_student:

            messages.error(
                request,
                "Only students can login here"
            )

            return render(
                request,
                "student/login.html"
            )


        login(
            request,
            user
        )


        return redirect(
            "student_dashboard"
        )


    return render(
        request,
        "student/login.html"
    )



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


        if user is None:

            messages.error(
                request,
                "Invalid username or password"
            )

            return render(
                request,
                "faculty/login.html"
            )


        if not user.is_faculty and not user.is_superuser:

            messages.error(
                request,
                "Only faculty can login here"
            )

            return render(
                request,
                "faculty/login.html"
            )


        login(
            request,
            user
        )


        return redirect(
            "faculty_dashboard"
        )


    return render(
        request,
        "faculty/login.html"
    )



# =========================================
# LOGOUT
# =========================================

def logout_view(request):

    logout(request)

    return redirect(
        "index"
    )



# =========================================
# FACULTY PERMISSION
# =========================================

def is_faculty(user):

    return (
        user.is_authenticated
        and
        (user.is_faculty or user.is_superuser)
    )



# =========================================
# FACULTY DASHBOARD
# =========================================

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):

    papers = QuestionPaper.objects.all().order_by(
        "-uploaded_at"
    )


    return render(
        request,
        "faculty/dashboard.html",
        {
            "papers": papers
        }
    )



# =========================================
# STUDENT DASHBOARD
# =========================================

@login_required
def student_dashboard(request):

    try:

        student = StudentProfile.objects.get(
            user=request.user
        )


        course_obj = Course.objects.filter(
            name__iexact=student.course
        ).first()


        quizzes = []


        if course_obj:

            quizzes = ActiveQuiz.objects.filter(
                course=course_obj,
                semester=student.semester,
                is_active=True
            )


        results = Result.objects.filter(
            student=request.user
        )


        context = {

            "student": student,

            "quizzes": quizzes,

            "results": results
        }


        return render(
            request,
            "student/dashboard.html",
            context
        )


    except StudentProfile.DoesNotExist:


        return render(
            request,
            "student/dashboard.html",
            {
                "error":
                "Student profile not found"
            }
        )



# =========================================
# VIEW QUESTIONS
# =========================================

@login_required
@user_passes_test(is_faculty)
def view_questions(request):

    questions = Question.objects.all().order_by(
        "-id"
    )


    return render(
        request,
        "faculty/view_questions.html",
        {
            "questions": questions
        }
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

            form.save()

            messages.success(
                request,
                "Question paper uploaded successfully."
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
# PASSWORD GENERATOR
# =========================================

@login_required
@user_passes_test(is_faculty)
def password_generator(request):

    return render(
        request,
        "faculty/password_generator.html"
    )



# =========================================
# RESULTS
# =========================================

@login_required
@user_passes_test(is_faculty)
def view_results(request):

    results = Result.objects.all().order_by(
        "-id"
    )


    return render(
        request,
        "faculty/results.html",
        {
            "results": results
        }
    )

# =========================================
# PUBLISH EXAM
# =========================================

# =========================================
# PUBLISH EXAM
# =========================================

@login_required
@user_passes_test(is_faculty)
def publish_exam(request, id):

    paper = QuestionPaper.objects.get(id=id)

    # Here you can add publishing logic later

    messages.success(
        request,
        f"{paper.subject} published successfully"
    )

    return redirect(
        "faculty_dashboard"
    )
@login_required
@user_passes_test(is_faculty)
def delete_paper(request, pk):

    paper = QuestionPaper.objects.get(pk=pk)

    paper.delete()

    messages.success(
        request,
        "Question paper deleted successfully."
    )

    return redirect("faculty_dashboard")
# =========================================
# ADMIN DASHBOARD
# =========================================

@staff_member_required
def admin_dashboard(request):

    context = {

        "student_count": User.objects.filter(is_student=True).count(),

        "faculty_count": User.objects.filter(is_faculty=True).count(),

        "course_count": Course.objects.count(),

        "paper_count": QuestionPaper.objects.count(),

        "question_count": Question.objects.count(),

        "published_exam_count": PublishedExam.objects.count(),

        "active_exam_count": ActiveQuiz.objects.filter(is_active=True).count(),

        "result_count": Result.objects.count(),

        "exams": PublishedExam.objects.order_by("-exam_date")[:5],

    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context
    )


# =========================================
# ADMIN MODULE PAGES
# =========================================

@staff_member_required
def manage_faculty(request):
    return render(request, "admin_panel/faculty_list.html")


@staff_member_required
def manage_students(request):
    return render(request, "admin_panel/student_list.html")


@staff_member_required
def manage_courses(request):
    return render(request, "admin_panel/course_list.html")


@staff_member_required
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

@staff_member_required
def manage_exams(request):
    return render(request, "admin_panel/published_exams.html")


@staff_member_required
def admin_reports(request):
    return render(request, "admin_panel/reports.html")



@staff_member_required
def manage_faculty(request):

    faculty = User.objects.filter(is_faculty=True).order_by("username")

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

# =========================================
# ADD FACULTY
# =========================================

@staff_member_required
def add_faculty(request):

    if request.method == "POST":

        form = FacultyRegistrationForm(request.POST)

        if form.is_valid():

            faculty = form.save(commit=False)

            faculty.is_faculty = True
            faculty.is_student = False
            faculty = form.save(commit=False)
            faculty.is_faculty = True
            faculty.is_student = False

            faculty.save()
            messages.success(request,"Faculty added successfully."
            )
            return redirect("manage_faculty")

    else:

        form = FacultyRegistrationForm()

    return render(
        request,
        "admin_panel/add_faculty.html",
        {
            "form": form
        }
    )
## =========================================
# EDIT STUDENT
# =========================================

@staff_member_required
def edit_student(request, id):

    student = get_object_or_404(User, id=id)

    if request.method == "POST":

        form = StudentRegistrationForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            student = form.save(commit=False)
            student.is_student = True
            student.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("manage_students")

    else:

        form = StudentRegistrationForm(instance=student)

    return render(
        request,
        "admin_panel/add_student.html",
        {
            "form": form
        }
    )
# =========================================
# STUDENT MANAGEMENT
# =========================================

@staff_member_required
def manage_students(request):

    students = User.objects.filter(is_student=True).order_by("username")

    print("TOTAL STUDENTS:", students.count())

    for s in students:
        print(
            s.username,
            s.course,
            s.semester
        )

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

@staff_member_required
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

@staff_member_required
def edit_subject(request, id):

    subject = get_object_or_404(Subject, id=id)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("manage_subjects")

    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "admin_panel/edit_subject.html",
        {
            "form": form
        }
    )

# =========================================
# DELETE STUDENT
# =========================================

@staff_member_required
def delete_subject(request, id):

    subject = get_object_or_404(Subject, id=id)

    subject.delete()

    messages.success(request, "Subject deleted successfully.")

    return redirect("manage_subjects")
# =========================================
# UPLOAD STUDENTS FROM EXCEL
# =========================================

import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import User

@staff_member_required
def upload_students(request):

    print("=" * 50)
    print("Method:", request.method)

    if request.method == "POST":

        print("POST RECEIVED")

        excel_file = request.FILES.get("excel_file")

        print("FILE:", excel_file)

        if not excel_file:
            messages.error(request, "Please select an Excel file.")
            return redirect("upload_students")

        try:

            df = pd.read_excel(excel_file)

            print("Columns:", df.columns.tolist())
            print(df.head())

            imported = 0
            skipped = 0

            for _, row in df.iterrows():

                print("Processing:", row.to_dict())

                username = str(row["Username"]).strip()

                if User.objects.filter(username=username).exists():
                    skipped += 1
                    continue

                user = User.objects.create_user(
                    username=username,
                    first_name=str(row["First Name"]),
                    last_name=str(row["Last Name"]),
                    email=str(row["Email"]),
                    password=str(row["Password"]),
                )

                user.course = str(row["Course"])
                user.semester = int(row["Semester"])
                user.is_student = True
                user.save()

                imported += 1

            print("Imported:", imported)
            print("Skipped:", skipped)

            messages.success(
                request,
                f"{imported} students imported successfully."
            )

            if skipped:
                messages.warning(
                    request,
                    f"{skipped} duplicate usernames skipped."
                )

            return redirect("manage_students")

        except Exception as e:

            import traceback
            traceback.print_exc()

            print("ERROR:", e)

            messages.error(request, str(e))

    return render(request, "admin_panel/upload_students.html")


@staff_member_required
def manage_courses(request):

    courses = Course.objects.all().order_by("name")

    return render(
        request,
        "admin_panel/course_list.html",
        {
            "courses": courses
        }
    )

@staff_member_required
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
@staff_member_required
def edit_course(request, id):

    course = Course.objects.get(id=id)

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
@staff_member_required
def delete_course(request, id):

    course = Course.objects.get(id=id)

    course.delete()

    messages.success(
        request,
        "Course deleted successfully."
    )

    return redirect("manage_courses")

# =========================================
# SUBJECT MANAGEMENT
# =========================================

@staff_member_required
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


@staff_member_required
def edit_subject(request, id):

    subject = get_object_or_404(Subject, id=id)

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


@staff_member_required
def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    subject.delete()

    messages.success(request, "Subject deleted successfully.")
    return redirect("manage_subjects")

@staff_member_required
def manage_subjects(request):
    subjects = Subject.objects.all().order_by("course", "semester", "name")

    return render(
        request,
        "admin_panel/subject_list.html",
        {
            "subjects": subjects
        }
    )
@staff_member_required
def edit_faculty(request, id):

    faculty = get_object_or_404(User, id=id)

    if request.method == "POST":

        form = FacultyRegistrationForm(
            request.POST,
            instance=faculty
        )

        if form.is_valid():

            faculty = form.save(commit=False)
            faculty.is_faculty = True
            faculty.is_student = False
            faculty.save()

            messages.success(
                request,
                "Faculty updated successfully."
            )

            return redirect("manage_faculty")

    else:

        form = FacultyRegistrationForm(instance=faculty)

    return render(
        request,
        "admin_panel/add_faculty.html",
        {
            "form": form
        }
    )
@staff_member_required
def delete_faculty(request, id):

    user = User.objects.get(id=id)

    # Delete faculty profile if it exists
    FacultyProfile.objects.filter(user=user).delete()

    user.delete()

    messages.success(
        request,
        "Faculty deleted successfully."
    )

    return redirect("manage_faculty")
@login_required
def question_bank(request):

    questions = Question.objects.all().order_by('-id')

    context = {
        "questions": questions
    }

    return render(
        request,
        "admin_panel/question_bank.html",
        context
    )
def upload_questions(request):

    if request.method == "POST":

        form = QuestionUploadForm(request.POST, request.FILES)

        if form.is_valid():

            subject = form.cleaned_data['subject']

            excel = request.FILES['excel_file']

            df = pd.read_excel(excel)


            for _, row in df.iterrows():

                Question.objects.create(

                    subject=subject,

                    question_text=row['question_text'],

                    option1=row['option1'],

                    option2=row['option2'],

                    option3=row['option3'],

                    option4=row['option4'],

                    correct_answer=row['correct_answer'],

                    marks=row['marks']

                )


            messages.success(
                request,
                "Questions uploaded successfully"
            )

            return redirect(
                'question_bank'
            )


    else:

        form = QuestionUploadForm()


    return render(
        request,
        "admin_panel/upload_questions.html",
        {
            "form":form
        }
    )

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

                    marks=row["marks"]

                )


            messages.success(
                request,
                "Questions uploaded successfully"
            )


            return redirect(
                "question_bank"
            )


    else:

        form = QuestionUploadForm()


    return render(
        request,
        "admin_panel/upload_questions.html",
        {
            "form": form
        }
    )