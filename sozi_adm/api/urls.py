from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MeetingViewSet, GeneralCandidateViewSet

router = DefaultRouter()

# router.register(r'candidate/(?P<id>\d+)', CandidateViewSet)
router.register(r'candidate', GeneralCandidateViewSet)

#   TODO: объединить вьюсеты

router.register('meeting', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
