from rest_framework import serializers

from meetings.models import Meeting
from users.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    is_register = serializers.SerializerMethodField(
        method_name='get_is_register'
    )

    class Meta:
        fields = ('email',
                  'name',
                  'telegram_ID',
                  'phone',
                  'category',
                  'is_register',)
        model = Candidate

    def get_is_register(self, obj):
        return Candidate.objects.filter(
            telegram_ID=obj.telegram_ID
        ).exists()


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('date_meeting',)
        model = Meeting
