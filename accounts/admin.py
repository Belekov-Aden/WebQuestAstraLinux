from django.contrib import admin

from .models import QuizResult, StageSevenProgress


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    pass


@admin.register(StageSevenProgress)
class StageSevenProgressAdmin(admin.ModelAdmin):
    pass
