from django.db import models
from django.contrib.auth.models import AbstractUser


# ==================================================
# CUSTOM USER
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
        blank=True,
        null=True
    )

    course = models.CharField(
        max_length=100
    )

    semester = models.IntegerField(
        default=1
    )


    def __str__(self):
        return self.name or self.user.username



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
# QUESTION BANK
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
        return self.question_text[:50]



# ==================================================
# QUESTION PAPER UPLOAD
# ==================================================

class QuestionPaper(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
    Course,
    on_delete=models.CASCADE,
    null=True,
    blank=True
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
        return self.subject.name

# ==================================================
# ACTIVE QUIZ
# ==================================================

class ActiveQuiz(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.IntegerField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    duration_minutes = models.IntegerField(default=60)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject.name} - {self.course.name}"

# ==================================================
# RESULT
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



# ==========================================================
# COURSE CONFIGURATION
# ==========================================================

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

    def __str__(self):
        return str(self.course)
# ==================================================
# EXAM
# ==================================================

class Exam(models.Model):

    exam_name = models.CharField(
        max_length=100
    )


    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )


    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )


    duration = models.IntegerField(
        default=60
    )


    number_of_questions = models.IntegerField()


    start_time = models.DateTimeField()


    end_time = models.DateTimeField()


    is_published = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.exam_name



# ==================================================
# EXAM QUESTIONS
# ==================================================

class ExamQuestion(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )


    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )


    class Meta:

        unique_together = (
            "exam",
            "question",
        )

        # ==================================================
# STUDENT ANSWER
# ==================================================

class StudentAnswer(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_answer = models.CharField(
        max_length=200
    )

    is_correct = models.BooleanField(
        default=False
    )

    marks_obtained = models.IntegerField(
        default=0
    )

    answered_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.student.username} - {self.question.id}"