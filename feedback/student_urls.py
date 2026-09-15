from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.student_feedback_list,
        name="student_feedback_list",
    ),

    path(
        "<int:assignment_id>/",
        views.student_feedback_form,
        name="student_feedback_form",
    ),

    path(
        "<int:assignment_id>/success/",
        views.student_feedback_success,
        name="student_feedback_success",
    ),
]