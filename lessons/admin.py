from django.contrib import admin
from .models import Language, Module, Lesson, Exercise

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'order')
    list_filter = ('language',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'xp_reward')
    list_filter = ('module',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'type')
    list_filter = ('type', 'lesson')
