from rest_framework import serializers
from .models import Language, Module, Lesson, Exercise, UserProgress


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'type', 'question', 'answer', 'options']


class LessonSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'xp_reward', 'exercises']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'description', 'lessons']


class LanguageSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'modules']


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'lesson', 'is_completed', 'completed_at']
        read_only_fields = ['lesson', 'is_completed', 'completed_at']
