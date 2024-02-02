import datetime as dt

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from meetings.models import Meeting
from users.models import Candidate

from .serializers import CandidateSerializer, MeetingSerializer


class GeneralCandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateViewSet(GeneralCandidateViewSet):

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        # print(Candidate.objects.get(telegram_ID=user_id))
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
        if date_in_db:
            if now < date_in_db.date_meeting.timestamp():
                return (Meeting.objects.last(), )
        return (Meeting(), )

    @action(detail=False, methods='patch')
    def patch(self, request):
        """Изменение информации об актуальной встрече."""

        actual_meeting = Meeting.objects.last()
        serializer = MeetingSerializer(
            actual_meeting, partial=True, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
