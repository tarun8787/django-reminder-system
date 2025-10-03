from rest_framework import serializers
from jobtracker.applications.models import JobApplication, Reminder

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['user']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'
        read_only_fields = ['user', 'is_sent']