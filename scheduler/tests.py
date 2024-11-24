from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Users, InterviewAvailability
from datetime import time, date

class InterviewAPITests(APITestCase):
    def setUp(self):
        self.candidate_user = User.objects.create(username="candidate_user")
        self.interviewer_user = User.objects.create(username="interviewer_user")
        
        self.candidate = Users.objects.create(user=self.candidate_user, user_type='Candidate')
        self.interviewer = Users.objects.create(user=self.interviewer_user, user_type='Interviewer')
        
        InterviewAvailability.objects.create(
            user=self.candidate,
            date=date.today(),
            start_time=time(9, 0),
            end_time=time(12, 0)
        )
        InterviewAvailability.objects.create(
            user=self.interviewer,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

    def test_register_user(self):
        response = self.client.post('/register_user/', {'name': 'new_user', 'user_type': 'Candidate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_type'], 'Candidate')

    def test_register_user_duplicate(self):
        response = self.client.post('/register_user/', {'name': 'candidate_user', 'user_type': 'Candidate'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Username already exists.", response.data['detail'])

    def test_get_users(self):
        response = self.client.get('/get_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_register_availability(self):
        payload = {
            "user": self.candidate.id,
            "start_time": "01:00 PM",
            "end_time": "03:00 PM",
            "date": date.today().isoformat()
        }
        response = self.client.post('/register_availability/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_availability_invalid_time(self):
        payload = {
            "user": self.candidate.id,
            "start_time": "03:00 PM",
            "end_time": "02:00 PM",
            "date": date.today().isoformat()
        }
        response = self.client.post('/register_availability/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("End time must be later than start time.", response.data['error'])

    def test_get_available_timeslots(self):
        response = self.client.get(
            '/get_availability/', 
            {'candidate': self.candidate.id, 'interviewer': self.interviewer.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("possible_slots", response.data)

    def test_get_available_timeslots_no_slots(self):
        InterviewAvailability.objects.filter(user=self.interviewer).update(
            start_time=time(1, 0), end_time=time(2, 0)
        )
        response = self.client.get(
            '/get_availability/', 
            {'candidate': self.candidate.id, 'interviewer': self.interviewer.id}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No available interview slots.", response.data['message'])
