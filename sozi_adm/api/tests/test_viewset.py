from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from datetime import date  # Добавили импорт date из datetime

from meetings.models import Meeting
from users.models import Candidate


class CandidateViewSetTests(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(name='Test Candidate',
                                                  telegram_ID='123')

    def test_get_candidate_list(self):
        url = reverse('candidate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_candidate(self):
        data = {'name': 'New Candidate', 'telegram_ID': '456'}
        url = reverse('candidate-list')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_candidate_detail(self):
        url = reverse('candidate-detail', args=[self.candidate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_action(self):
        url = reverse('candidate-check', args=[self.candidate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MeetingViewSetTests(TestCase):
    def setUp(self):
        self.meeting = Meeting.objects.create(location='Test Meeting',
                                              date_meeting=date.today())

    def test_get_meeting_list(self):
        url = reverse('meeting-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_meeting_detail(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
