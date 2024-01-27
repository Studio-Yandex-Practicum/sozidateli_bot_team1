import datetime as dt

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from meetings.models import Meeting
from users.models import Candidate
from .serializers import CandidateSerializer, MeetingSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        try:
            return (Candidate.objects.get(telegram_ID=user_id), )
        except Candidate.DoesNotExist:
            return (Candidate(), )

    @action(detail=True, methods='patch')
    def patch(self, request, id):

        user = Candidate.objects.get(telegram_ID=id)
        serializer = CandidateSerializer(user, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeetingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        date_in_db = Meeting.objects.last()
        now = dt.datetime.now().timestamp()
        # date_in_db = dt.datetime.strptime(
        #         date_in_db.date_meeting, "%Y-%m-%dT%H:%M:%SZ"
        #     )
        if now < date_in_db.date_meeting.timestamp():
            return (Meeting.objects.last(), )
        return (Meeting(), )
