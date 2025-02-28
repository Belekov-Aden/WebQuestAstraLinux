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

class StageSevenProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_initiation = models.BooleanField(default=False)
    token_command_line = models.BooleanField(default=False)
    file_knowledge = models.BooleanField(default=False)
    security_shield = models.BooleanField(default=False)
    settings_key = models.BooleanField(default=False)
    optimization_badge = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Прогресс этапа 7'
        verbose_name_plural = 'Прогресс этапов 7'