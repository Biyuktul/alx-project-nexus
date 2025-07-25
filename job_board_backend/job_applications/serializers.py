from rest_framework import serializers
from jobs.models import Job
from .models import Application
from jobs.serializers import JobSerializer
from authentication.models import User

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='job', write_only=True
    )
    applicant = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'job', 'job_id', 'application_letter', 'status', 'application_time']
        read_only_fields = ['applicant', 'application_time']

    def create(self, validated_data):
        validated_data['applicant'] = self.context['request'].user
        validated_data['status'] = 'submitted' #will be changed in the future to be used from the status choice in the application model
        return super().create(validated_data)