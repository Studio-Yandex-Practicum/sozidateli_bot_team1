from rest_framework import serializers

from meetings.models import Meeting
from users.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',
                  'name',
                  'telegram_ID',
                  'phone',
                  'category',
                  'confirm_date',)
        model = Candidate


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('date_meeting', 'location')
        model = Meeting
