from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True) # e.g., 'es' for Spanish

    def __str__(self):
        return self.name

class Module(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.language.code.upper()} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    xp_reward = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class Exercise(models.Model):
    EXERCISE_TYPES = (
        ('translate', 'Translation'),
        ('mcq', 'Multiple Choice'),
        ('fill', 'Fill in the Blank'),
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    question = models.TextField()
    answer = models.TextField()
    options = models.JSONField(default=dict, blank=True) # For MCQ options

    def __str__(self):
        return f"Exercise for {self.lesson.title}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
