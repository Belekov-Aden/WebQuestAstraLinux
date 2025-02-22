from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
        ]
    )
    score = models.IntegerField()
    total_questions = models.IntegerField(null=True)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Этап {self.step}: {self.user.username} - {self.score}/{self.total_questions}"

    class Meta:
        verbose_name = 'Результаты по квестам'
