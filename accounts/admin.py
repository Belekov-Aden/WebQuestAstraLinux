from django.contrib import admin

from .models import QuizResult


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    pass
