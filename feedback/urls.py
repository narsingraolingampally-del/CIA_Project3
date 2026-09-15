from django.urls import path

from . import views


urlpatterns = [

    # ========================================================
    # ADMIN FEEDBACK DASHBOARD
    # ========================================================

    path(
        "",
        views.feedback_admin_dashboard,
        name="feedback_admin_dashboard",
    ),


    # ========================================================
    # FEEDBACK FORMS
    # ========================================================

    path(
        "forms/",
        views.feedback_forms,
        name="feedback_forms",
    ),

    path(
        "forms/create/",
        views.create_feedback_form,
        name="create_feedback_form",
    ),

    path(
        "forms/<int:pk>/edit/",
        views.edit_feedback_form,
        name="edit_feedback_form",
    ),

    path(
        "forms/<int:pk>/toggle/",
        views.toggle_feedback_form,
        name="toggle_feedback_form",
    ),

    path(
        "forms/<int:pk>/delete/",
        views.delete_feedback_form,
        name="delete_feedback_form",
    ),


    # ========================================================
    # FEEDBACK QUESTIONS
    # ========================================================

    path(
        "forms/<int:form_id>/questions/",
        views.feedback_questions,
        name="feedback_questions",
    ),

    path(
        "forms/<int:form_id>/questions/add/",
        views.add_feedback_question,
        name="add_feedback_question",
    ),

    path(
        "questions/<int:pk>/edit/",
        views.edit_feedback_question,
        name="edit_feedback_question",
    ),

    path(
        "questions/<int:pk>/toggle/",
        views.toggle_feedback_question,
        name="toggle_feedback_question",
    ),

    path(
        "questions/<int:pk>/delete/",
        views.delete_feedback_question,
        name="delete_feedback_question",
    ),

    # Excel upload
    path(
        "forms/<int:form_id>/questions/upload/",
        views.upload_feedback_questions,
        name="upload_feedback_questions",
    ),

    # Excel template
    path(
        "forms/<int:form_id>/questions/template/",
        views.download_feedback_question_template,
        name="download_feedback_question_template",
    ),


    # ========================================================
    # FEEDBACK ASSIGNMENTS
    # ========================================================

    # Assignment list
    path(
        "assignments/",
        views.feedback_assignments,
        name="feedback_assignments",
    ),

    # Individual assignment
    path(
        "assignments/create/",
        views.create_feedback_assignment,
        name="create_feedback_assignment",
    ),

    # Bulk assignment to all teaching faculty
    path(
        "assignments/bulk-create/",
        views.bulk_create_feedback_assignments,
        name="bulk_create_feedback_assignments",
    ),

    # Activate / deactivate assignment
    path(
        "assignments/<int:pk>/toggle/",
        views.toggle_feedback_assignment,
        name="toggle_feedback_assignment",
    ),

    # Delete assignment
    path(
        "assignments/<int:pk>/delete/",
        views.delete_feedback_assignment,
        name="delete_feedback_assignment",
    ),


    # ========================================================
    # FEEDBACK REPORTS
    # ========================================================

    path(
        "reports/",
        views.feedback_reports,
        name="feedback_reports",
    ),

    path(
        "reports/export/",
        views.export_feedback_reports,
        name="export_feedback_reports",
    ),

]