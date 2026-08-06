from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import export_results


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        views.index_page,
        name='index'
    ),


    # =====================================================
    # LOGIN
    # =====================================================

    path(
        'admin-login/',
        views.admin_login,
        name='admin_login'
    ),

    path(
        'faculty-login/',
        views.faculty_login,
        name='faculty_login'
    ),

    path(
        'student/login/',
        views.student_login,
        name='student_login'
    ),


    # =====================================================
    # DASHBOARDS
    # =====================================================

    path(
        'admin-panel/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'faculty-dashboard/',
        views.faculty_dashboard,
        name='faculty_dashboard'
    ),

    path(
        'student-dashboard/',
        views.student_dashboard,
        name='student_dashboard'
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =====================================================
    # STUDENT EXAM
    # =====================================================

    path(
        'take-exam/<int:exam_id>/',
        views.take_exam,
        name='take_exam'
    ),

    path(
        'submit-exam/',
        views.submit_exam,
        name='submit_exam'
    ),

    path(
        "student/upcoming-exams/",
        views.student_upcoming_exams,
        name="student_upcoming_exams"
    ),

    path(
        "student/results/",
        views.student_results,
        name="student_results"
    ),



    # =====================================================
    # FACULTY
    # =====================================================

    path(
        'faculty-dashboard/',
        views.faculty_dashboard,
        name='faculty_dashboard'
    ),

    path(
        'view-questions/',
        views.view_questions,
        name='view_questions'
    ),

    path(
        'faculty/upload-questions/',
        views.faculty_upload_questions,
        name='faculty_upload_questions'
    ),

    path(
        'upload-question-paper/',
        views.upload_question_paper,
        name='upload_question_paper'
    ),

    path(
        'faculty/edit-question/<int:pk>/',
        views.faculty_edit_question,
        name='faculty_edit_question'
    ),

    path(
        'faculty/delete-question/<int:pk>/',
        views.delete_question,
        name='delete_question'
    ),

    path(
        'faculty/delete-all-questions/',
        views.delete_all_questions,
        name='delete_all_questions'
    ),

    path(
        'faculty/password-generator/',
        views.password_generator,
        name='password_generator'
    ),


    path(
        'view-results/',
        views.view_results,
        name='view_results'
    ),

    path(
        'export-results/',
        export_results,
        name='export_results'
    ),


    # =====================================================
    # EXAM MANAGEMENT
    # =====================================================

    path(
        "faculty/create-exam/",
        views.create_exam,
        name="create_exam"
    ),

    path(
        "admin-panel/exams/",
        views.manage_exams,
        name="manage_exams"
    ),

    path(
        "admin-panel/exams/create/",
        views.admin_create_exam,
        name="admin_create_exam"
    ),

    path(
        "admin-panel/exams/edit/<int:id>/",
        views.edit_exam,
        name="edit_exam"
    ),

    path(
        "admin-panel/exams/<int:exam_id>/questions/",
        views.view_exam_questions,
        name="view_exam_questions"
    ),

    path(
        "publish-exam/<int:id>/",
        views.publish_exam,
        name="publish_exam"
    ),

    path(
        "admin-panel/unpublish-exam/<int:id>/",
        views.unpublish_exam,
        name="unpublish_exam"
    ),

    path(
        "admin-panel/published-exams/",
        views.published_exams,
        name="published_exams"
    ),



    # =====================================================
    # FACULTY MANAGEMENT
    # =====================================================

    path(
        'admin-panel/faculty/',
        views.manage_faculty,
        name='manage_faculty'
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

    path(
        "admin-panel/upload-faculty/",
        views.upload_faculty,
        name="upload_faculty"
    ),



    # =====================================================
    # STUDENT MANAGEMENT
    # =====================================================

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
        'admin-panel/students/delete/<int:id>/',
        views.delete_student,
        name='delete_student'
    ),

    path(
        'admin-panel/students/upload/',
        views.upload_students,
        name='upload_students'
    ),

    path(
        'admin-panel/students/delete-selected/',
        views.delete_selected_students,
        name='delete_selected_students'
    ),



    # =====================================================
    # COURSE
    # =====================================================

    path(
        'admin-panel/courses/',
        views.manage_courses,
        name='manage_courses'
    ),

    path(
        'admin-panel/courses/add/',
        views.add_course,
        name='add_course'
    ),

    path(
        'admin-panel/courses/edit/<int:id>/',
        views.edit_course,
        name='edit_course'
    ),

    path(
        'admin-panel/courses/delete/<int:id>/',
        views.delete_course,
        name='delete_course'
    ),



    # =====================================================
    # SUBJECT
    # =====================================================

    path(
        'admin-panel/subjects/',
        views.manage_subjects,
        name='manage_subjects'
    ),

    path(
        'admin-panel/subjects/add/',
        views.add_subject,
        name='add_subject'
    ),

    path(
        'admin-panel/subjects/edit/<int:id>/',
        views.edit_subject,
        name='edit_subject'
    ),

    path(
        'admin-panel/subjects/delete/<int:id>/',
        views.delete_subject,
        name='delete_subject'
    ),



    # =====================================================
    # QUESTION BANK
    # =====================================================

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

    path(
        'admin-panel/question-bank/edit/<int:pk>/',
        views.edit_question,
        name='edit_question'
    ),

    path(
        'admin-panel/question-bank/delete/<int:pk>/',
        views.delete_question,
        name='delete_question'
    ),



    # =====================================================
    # REPORTS
    # =====================================================

    path(
        'admin-panel/reports/',
        views.admin_reports,
        name='admin_reports'
    ),

    path(
        "admin-panel/reports/export/excel/",
        views.export_reports_excel,
        name="export_reports_excel"
    ),

    path(
        "admin-panel/reports/export/pdf/",
        views.export_reports_pdf,
        name="export_reports_pdf"
    ),



    # =====================================================
    # AJAX
    # =====================================================

    path(
        "ajax/load-subjects/",
        views.load_subjects,
        name="ajax_load_subjects"
    ),



    # =====================================================
    # DOWNLOAD
    # =====================================================

    path(
        "download-question-template/",
        views.download_question_template,
        name="download_question_template"
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )