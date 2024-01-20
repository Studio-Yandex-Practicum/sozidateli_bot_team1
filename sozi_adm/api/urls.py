from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CandidateViewSet, MeetingViewSet

router = DefaultRouter()

router.register('candidate', CandidateViewSet)
router.register('meeting', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
