from django.db import models
from django.contrib.auth.models import AbstractUser



# ==================================================
# CUSTOM USER MODEL
# ==================================================

class User(AbstractUser):

    is_student = models.BooleanField(default=False)

    is_faculty = models.BooleanField(default=False)

    course = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    semester = models.IntegerField(
        default=1,
        blank=True,
        null=True
    )


    def __str__(self):
        return self.username



# ==================================================
# COURSE
# ==================================================

class Course(models.Model):

    name = models.CharField(
        max_length=100
    )


    def __str__(self):
        return self.name


# ==================================================
# SUBJECT
# ==================================================


    
class Subject(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"

# ==================================================
# STUDENT PROFILE
# ==================================================

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    course = models.CharField(
        max_length=100
    )

    semester = models.IntegerField(
        default=1
    )


    def __str__(self):
        return f"{self.name} - {self.course}"



# ==================================================
# FACULTY PROFILE
# ==================================================

class FacultyProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )


    def __str__(self):
        return self.name



# ==================================================
# QUESTIONS
# ==================================================

# ==================================================
# QUESTIONS
# ==================================================

class Question(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    question_text = models.TextField()

    option1 = models.CharField(
        max_length=200
    )

    option2 = models.CharField(
        max_length=200
    )

    option3 = models.CharField(
        max_length=200
    )

    option4 = models.CharField(
        max_length=200
    )

    correct_answer = models.CharField(
        max_length=200
    )

    marks = models.IntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.subject.code} - {self.question_text[:50]}"


# ==================================================
# ACTIVE QUIZ
# ==================================================

class ActiveQuiz(models.Model):

    subject = models.CharField(
        max_length=100
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.IntegerField()


    start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )


    duration_minutes = models.IntegerField(
        default=30
    )


    is_active = models.BooleanField(
        default=False
    )


    def __str__(self):
        return f"{self.subject} - {self.course}"



class QuestionPaper(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.IntegerField()

    duration_minutes = models.IntegerField(
        default=30
    )

    file = models.FileField(
        upload_to="papers/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.subject.name} ({self.course.name})"
# ==================================================
# RESULTS
# ==================================================

class Result(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    quiz = models.ForeignKey(
        ActiveQuiz,
        on_delete=models.CASCADE,
        null=True
    )


    score = models.IntegerField()


    total_marks = models.IntegerField(
        default=0
    )


    completed_at = models.DateTimeField(
        auto_now_add=True
    )



# ==================================================
# PUBLISHED EXAM
# ==================================================

class PublishedExam(models.Model):

    subject = models.CharField(
        max_length=100
    )

    course = models.CharField(
        max_length=100
    )

    semester = models.IntegerField()


    exam_date = models.DateTimeField(
        auto_now_add=True
    )



# ==================================================
# COURSE CONFIGURATION
# ==================================================

class CourseConfig(models.Model):

    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    is_open = models.BooleanField(
        default=True
    )