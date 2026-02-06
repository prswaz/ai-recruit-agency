from django.conf import settings
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255, unique=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=2048, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_url = models.URLField(max_length=2048, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True) # Full-time, etc.
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Normalized Skills
    skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    
    # Keep lightweight attributes as JSON
    requirements = models.JSONField(default=list, blank=True) 
    benefits = models.JSONField(default=list, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"
