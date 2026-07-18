from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from .models import (
    User, StudentProfile, Course, ActiveQuiz, 
    PublishedExam, Question, Result, CourseConfig, QuestionPaper
)

# --- 1. BULK ACTIONS ---
@admin.action(description="Publish selected exams")
def publish_exams(modeladmin, request, queryset):
    for exam in queryset:
        exam.is_active = True
        exam.save()
        PublishedExam.objects.get_or_create(
            subject=str(exam.subject),
            course=str(exam.course.name),
            semester=exam.semester
        )
    messages.success(request, "Selected exams have been published.")

@admin.action(description="Withdraw selected exams")
def withdraw_exams(modeladmin, request, queryset):
    for exam in queryset:
        exam.is_active = False
        exam.save()
        PublishedExam.objects.filter(subject=exam.subject, semester=exam.semester).delete()
    messages.warning(request, "Selected exams have been withdrawn.")

# --- 2. CUSTOM ADMIN CLASSES ---

@admin.register(ActiveQuiz)
class ActiveQuizAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'semester', 'start_time', 'end_time', 'is_active', 'exam_status', 'publish_button')
    list_filter = ('course', 'semester', 'is_active')
    actions = [publish_exams, withdraw_exams]

    # This injects custom CSS to make the buttons and badges look better
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',)
        }

    def exam_status(self, obj):
        now = timezone.now()
        # Using inline styles for quick results without external CSS files
        base_style = "padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: bold; text-transform: uppercase;"
        
        if not obj.is_active: 
            return mark_safe(f'<span style="{base_style} background-color: #e9ecef; color: #6c757d;">● Draft</span>')
        
        if obj.start_time and now < obj.start_time: 
            return mark_safe(f'<span style="{base_style} background-color: #fff3cd; color: #856404;">● Scheduled</span>')
        
        if obj.start_time and obj.end_time and obj.start_time <= now <= obj.end_time:
            # Added a slight animation effect simulation with bold colors
            return mark_safe(f'<span style="{base_style} background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;">● LIVE NOW</span>')
        
        return mark_safe(f'<span style="{base_style} background-color: #f8d7da; color: #721c24;">● Expired</span>')
    
    exam_status.short_description = "Live Status"

    def publish_button(self, obj):
        btn_style = "padding: 5px 12px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 11px; display: inline-block;"
        
        if not obj.is_active:
            url = f"/admin/quiz/activequiz/{obj.pk}/publish/"
            return format_html(
                '<a class="button" style="{} background-color: #28a745; color: white;" href="{}">PUBLISH</a>', 
                btn_style, url
            )
        
        url = f"/admin/quiz/activequiz/{obj.pk}/withdraw/"
        return format_html(
            '<a class="button" style="{} background-color: #6c757d; color: white;" href="{}">WITHDRAW</a>', 
            btn_style, url
        )

    # ... keep the rest of your get_urls, process_publish, and process_withdraw methods ...
    def publish_button(self, obj):
        if not obj.is_active:
            url = f"/admin/quiz/activequiz/{obj.pk}/publish/"
            return format_html('<a class="button" style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;" href="{}">Publish Now</a>', url)
        url = f"/admin/quiz/activequiz/{obj.pk}/withdraw/"
        return format_html('<a class="button" style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;" href="{}">Withdraw</a>', url)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/publish/', self.process_publish, name='publish_single'),
            path('<int:pk>/withdraw/', self.process_withdraw, name='withdraw_single'),
        ]
        return custom_urls + urls

    def process_publish(self, request, pk):
        exam = self.get_object(request, pk)
        exam.is_active = True
        exam.save()
        PublishedExam.objects.get_or_create(
            subject=str(exam.subject), 
            course=str(exam.course.name), 
            semester=exam.semester
        )
        messages.success(request, f"Exam {exam.subject} is now Published.")
        return redirect('admin:quiz_activequiz_changelist')

    def process_withdraw(self, request, pk):
        exam = self.get_object(request, pk)
        exam.is_active = False
        exam.save()
        PublishedExam.objects.filter(subject=exam.subject, semester=exam.semester).delete()
        messages.warning(request, f"Exam {exam.subject} has been Withdrawn.")
        return redirect('admin:quiz_activequiz_changelist')

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'semester', 'uploaded_at')
    list_filter = ('course', 'semester')
    search_fields = ('subject',)

@admin.register(PublishedExam)
class PublishedExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'semester', 'exam_date')
    readonly_fields = ('subject', 'course', 'semester', 'exam_date')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "question_text",
        "correct_answer",
        "marks",
    )

    list_filter = (
        "subject",
    )

    search_fields = (
        "question_text",
        "subject__name",
        "subject__code",
    )

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score')
    list_filter = ('quiz__course', 'quiz__subject')
    search_fields = ('student__username', 'quiz__subject')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'course', 'semester')
    list_filter = ('course', 'semester')
    search_fields = ('user__username', 'name')

# --- 3. THE REST OF THE TABS ---

admin.site.register(User)
admin.site.register(Course)
admin.site.register(CourseConfig)