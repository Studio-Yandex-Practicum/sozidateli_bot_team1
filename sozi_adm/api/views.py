from rest_framework import viewsets
from rest_framework.decorators import action

from meetings.models import Meeting
from users.models import Candidate
from .serializers import CandidateSerializer, MeetingSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(
        methods=['GET'],
        url_name='check',
        url_path='check',
        detail=True
    )
    def get_queryset(self):
        user_id = self.kwargs.get('id')
        try:
            return (Candidate.objects.get(telegram_ID=user_id), )
        except Candidate.DoesNotExist:
            return (Candidate(), )


class MeetingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return (Meeting.objects.last(), )
