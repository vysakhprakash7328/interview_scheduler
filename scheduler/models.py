from django.db import models
from django.contrib.auth.models import User

USERTYPE = (
    ('Interviewer', 'Interviewer'),
    ('Candidate', 'Candidate'),
)

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.user_type}"

class InterviewAvailability(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{str(self.user.user.first_name)}-{str(self.date)}"