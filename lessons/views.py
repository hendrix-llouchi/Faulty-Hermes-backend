from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Language, Module, Lesson, Exercise
from .serializers import (
    LanguageSerializer,
    ModuleSerializer,
    LessonSerializer,
    ExerciseSerializer,
)


class LanguageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Returns a list of all languages and their full nested content tree
    (modules → lessons → exercises).
    """
    queryset = Language.objects.prefetch_related(
        'modules__lessons__exercises'
    ).all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ModuleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Module.objects.select_related('language').prefetch_related(
        'lessons__exercises'
    ).all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LessonViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Lesson.objects.select_related('module').prefetch_related(
        'exercises'
    ).all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ExerciseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Exercise.objects.select_related('lesson').all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
