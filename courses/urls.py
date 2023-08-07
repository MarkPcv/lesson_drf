from django.urls import path
from rest_framework import routers

from courses.apps import CoursesConfig
from courses.views import LessonListAPIView, LessonCreateAPIView, \
    LessonRetrieveAPIView, LessonUpdateAPIView, CourseViewSet, \
    PaymentListAPIView

app_name = CoursesConfig.name

router = routers.DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', LessonUpdateAPIView.as_view(), name='lesson-delete'),

    # payments
    path('payments/', PaymentListAPIView.as_view(), name='payments-list'),
] + router.urls
