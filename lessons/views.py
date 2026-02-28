from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Language, Module, Lesson, Exercise, UserProgress
from .serializers import (
    LanguageSerializer,
    ModuleSerializer,
    LessonSerializer,
    ExerciseSerializer,
    UserProgressSerializer,
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


class LogProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response(
                {'error': 'lesson_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'is_completed': True}
        )
        serializer = UserProgressSerializer(progress)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=http_status)
