from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Move quiz.urls ABOVE auth.urls so your custom login is found first
    path('', include('quiz.urls')), 
    path('', include('django.contrib.auth.urls')), 
]