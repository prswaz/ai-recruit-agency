from rest_framework import serializers
from .models import Company, Job, Skill

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ('user',)

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    skills = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Skill.objects.all(),
        required=False
    )
    # Just returning the ID for company write
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True, required=False
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company_id', 'company_name', 'location', 
            'type', 'experience_level', 'salary_range', 
            'description', 'requirements', 'benefits', 'skills', 'created_at'
        ]
    
    def get_company_name(self, obj):
        return obj.company.name if obj.company else 'Unknown Company'
