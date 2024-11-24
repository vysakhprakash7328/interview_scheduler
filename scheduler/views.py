from rest_framework.views import APIView
from . serializers import Interview_serializer, User_serializer, Get_user_serializer
from rest_framework.response import Response
from .models import InterviewAvailability, Users
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth.models import User




class Register_user(APIView):
    def post(self, request):
        username = request.data.get('name')
        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists."}, status=400)

        user_instance = User.objects.create(username=username)
        request.data['user'] = user_instance.id
        serializer = User_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    
    
class Get_users(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = Get_user_serializer(users, many=True)
        return Response(serializer.data)

class Register_Availability(APIView):
    def post(self, request):
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")
        user = request.data.get('user')
        if not  Users.objects.filter(id = user).exists():
            return Response({"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            start_time = datetime.strptime(start_time, '%I:%M %p').time()
            end_time = datetime.strptime(end_time, '%I:%M %p').time()
            
            if start_time >= end_time:
                return Response({"error": "End time must be later than start time."}, status=status.HTTP_400_BAD_REQUEST)
            request.data['start_time'] = start_time
            request.data['end_time'] = end_time
            
            serializer = Interview_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid time format. Please use 'HH:MM AM/PM'."}, status=status.HTTP_400_BAD_REQUEST)
    
class Get_Available_Timeslots(APIView):
    def get(self, request):
        candidate_id = request.query_params.get('candidate')
        interviewer_id = request.query_params.get('interviewer')

        if not candidate_id or not interviewer_id:
            return Response({'error': 'Candidate and interviewer are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            candidate_available_timeslots = InterviewAvailability.objects.filter(user__id=candidate_id, user__user_type='Candidate')
            interviewer_available_timeslots = InterviewAvailability.objects.filter(user__id=interviewer_id, user__user_type='Interviewer')
        except InterviewAvailability.DoesNotExist:
            return Response({"error": "Invalid candidate or interviewer ID."}, status=404)
        
        if not candidate_available_timeslots.exists() or not interviewer_available_timeslots.exists():
            return Response({"error": "Availability not found for either candidate or interviewer."}, status=404)

        possible_slots = {}

        for candidate in candidate_available_timeslots:
            for interviewer in interviewer_available_timeslots:
                if candidate.date == interviewer.date:
                    start_time = max(candidate.start_time, interviewer.start_time)
                    end_time = min(candidate.end_time, interviewer.end_time)
                    if start_time < end_time:
                        start_datetime = datetime.combine(candidate.date, start_time)
                        end_datetime = datetime.combine(candidate.date, end_time)

                        if candidate.date not in possible_slots:
                            possible_slots[candidate.date.isoformat()] = list()

                        while start_datetime + timedelta(hours=1) <= end_datetime:
                            start_time_str = start_datetime.strftime('%I:%M %p')
                            end_time_str = (start_datetime + timedelta(hours=1)).strftime('%I:%M %p')
                            
                            possible_slots[candidate.date.isoformat()].append((start_time_str, end_time_str))
                            
                            start_datetime += timedelta(hours=1)
        if possible_slots:
            return Response({"success": True, "possible_slots": possible_slots})
        else:
            return Response({"message": "No available interview slots."}, status=404)

   





