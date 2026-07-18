from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static



from . import views

urlpatterns = [

    # ===================================
    # HOME
    # ===================================

    path('', views.index_page, name='index'),

    # ===================================
    # LOGIN
    # ===================================

    path('faculty-login/', views.faculty_login, name='faculty_login'),

    path('student-login/', views.student_login, name='student_login'),

    # ===================================
    # DASHBOARDS
    # ===================================

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),

    # ===================================
    # FACULTY MODULE
    # ===================================

    path('view-questions/', views.view_questions, name='view_questions'),

    path('upload-question-paper/', views.upload_question_paper, name='upload_question_paper'),

    path('password-generator/', views.password_generator, name='password_generator'),

    path('view-results/', views.view_results, name='view_results'),

    path('publish-exam/<int:id>/', views.publish_exam, name='publish_exam'),

    path('delete-paper/<int:pk>/', views.delete_paper, name='delete_paper'),

    # ===================================
    # ADMIN PANEL
    # ===================================

    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),

    path('admin-panel/faculty/', views.manage_faculty, name='manage_faculty'),

    path('admin-panel/students/', views.manage_students, name='manage_students'),

    path('admin-panel/courses/', views.manage_courses, name='manage_courses'),

    path('admin-panel/subjects/', views.manage_subjects, name='manage_subjects'),

    path('admin-panel/exams/', views.manage_exams, name='manage_exams'),

    path('admin-panel/reports/', views.admin_reports, name='admin_reports'),

    # ===================================
    # LOGOUT
    # ===================================

    path(
        'logout/',
        LogoutView.as_view(next_page='index'),
        name='logout'
    ),
    path(
    'admin-panel/faculty/add/',
    views.add_faculty,
    name='add_faculty'
),
path(
    'admin-panel/faculty/edit/<int:id>/',
    views.edit_faculty,
    name='edit_faculty'
),

path(
    'admin-panel/faculty/delete/<int:id>/',
    views.delete_faculty,
    name='delete_faculty'
),

# ==========================================
# STUDENT MANAGEMENT
# ==========================================

path(
    'admin-panel/students/',
    views.manage_students,
    name='manage_students'
),

path(
    'admin-panel/students/add/',
    views.add_student,
    name='add_student'
),

path(
    'admin-panel/students/edit/<int:id>/',
    views.edit_student,
    name='edit_student'
),


path(
    'admin-panel/students/edit/<int:id>/',
    views.edit_student,
    name='edit_student'
),

path(
    'admin-panel/students/upload/',
    views.upload_students,
    name='upload_students'
),
path(
    "admin-panel/courses/",
    views.manage_courses,
    name="manage_courses"
),

path(
    "admin-panel/courses/add/",
    views.add_course,
    name="add_course"
),

path(
    "admin-panel/courses/edit/<int:id>/",
    views.edit_course,
    name="edit_course"
),

path(
    "admin-panel/courses/delete/<int:id>/",
    views.delete_course,
    name="delete_course"
),
path(
    "admin-panel/subjects/add/",
    views.add_subject,
    name="add_subject"
),

path(
    "admin-panel/subjects/edit/<int:id>/",
    views.edit_subject,
    name="edit_subject"
),

path(
    "admin-panel/subjects/delete/<int:id>/",
    views.delete_subject,
    name="delete_subject"
),
path(
    'admin-panel/question-bank/',
    views.question_bank,
    name='question_bank'
),
path(
    'admin-panel/question-bank/upload/',
    views.upload_questions,
    name='upload_questions'
),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)