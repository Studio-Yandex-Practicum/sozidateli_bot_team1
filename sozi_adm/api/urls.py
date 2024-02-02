from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GeneralCandidateViewSet, MeetingViewSet

router = DefaultRouter()

# router.register(r'candidate/(?P<id>\d+)', CandidateViewSet)
router.register(r'candidate', GeneralCandidateViewSet)

#   TODO: объединить вьюсеты

router.register('meeting', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
