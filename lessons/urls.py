from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, ModuleViewSet, LessonViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'exercises', ExerciseViewSet, basename='exercise')

urlpatterns = router.urls
