from rest_framework import serializers

from .models import InterviewAvailability, Users

class Interview_serializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewAvailability
        fields = '__all__'

        
class User_serializer(serializers.ModelSerializer):   
    class Meta:
        model = Users
        fields = '__all__'
        
class Get_user_serializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Users
        fields = '__all__'