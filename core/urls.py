from django.urls import include, path


urlpatterns = [

    # Admin Feedback Management
    path(
        "admin-panel/feedback/",
        include("feedback.urls"),
    ),

    # Student Feedback
    path(
        "student/feedback/",
        include("feedback.student_urls"),
    ),

    # Existing CIA Examination System
    path(
        "",
        include("quiz.urls"),
    ),
]