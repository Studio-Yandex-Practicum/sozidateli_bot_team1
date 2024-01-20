from rest_framework import serializers

from meetings.models import Meeting
from users.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',
                  'name',
                  'telegram_ID',
                  'phone',
                  'category',)
        model = Candidate


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('date_meeting',)
        model = Meeting
