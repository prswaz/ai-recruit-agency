from rest_framework import serializers
from .models import Candidate, Application, Interview, Recommendation, ResumeAnalysis
from core.serializers import JobSerializer
from core.models import Skill, Job

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all()
    )
    class Meta:
        model = Candidate
        fields = '__all__'
        read_only_fields = ('user',)

class ApplicationSerializer(serializers.ModelSerializer):
    # Allow clients to provide a job by its PK on create/update, but return
    # a full nested job representation when reading.
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        source='job', queryset=Job.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('candidate',)

class InterviewSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='application.job.title', read_only=True)
    company_name = serializers.CharField(source='application.job.company.name', read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Recommendation
        fields = '__all__'

class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = '__all__'
