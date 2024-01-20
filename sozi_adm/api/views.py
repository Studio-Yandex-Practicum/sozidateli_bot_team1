from rest_framework import viewsets

from meetings.models import Meeting
from users.models import Candidate
from .serializers import CandidateSerializer, MeetingSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class MeetingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return (Meeting.objects.last(), )
