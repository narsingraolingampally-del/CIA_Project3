from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redirect /admin/ to your custom admin dashboard
    path(
        "admin/",
        lambda request: redirect("admin_dashboard"),
        name="admin_redirect",
    ),

    # Your application URLs
    path("", include("quiz.urls")),
]