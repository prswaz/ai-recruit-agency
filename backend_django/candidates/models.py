from django.db import models
from django.conf import settings
from core.models import Job, Skill

class Candidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255) # Contact email, can be different from user.email
    phone = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    
    # URLs
    resume_url = models.URLField(max_length=2048, blank=True, null=True)
    linkedin_url = models.URLField(max_length=2048, blank=True, null=True)
    portfolio_url = models.URLField(max_length=2048, blank=True, null=True)
    
    # Normalized Skills (Many-to-Many)
    skills = models.ManyToManyField(Skill, related_name='candidates', blank=True)
    
    # AI Analysis Cache
    analysis_report = models.JSONField(default=dict, blank=True) # Logic/reasoning from AI
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interviewing', 'Interviewing'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='applied')
    source = models.CharField(max_length=50, default='web')
    
    # AI Scoring
    ai_score = models.FloatField(blank=True, null=True) # 0.0 - 100.0
    ai_feedback = models.TextField(blank=True, null=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')

class Interview(models.Model):
    RESULT_CHOICES = (
        ('pending', 'Pending'),
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    )
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    
    # Link to User (Recruiter) or null for AI
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews_conducted')
    
    scheduled_time = models.DateTimeField()
    meeting_link = models.URLField(max_length=2048, blank=True, null=True)
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True, null=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Recommendation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommendations')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='recommendations')
    match_score = models.FloatField()
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ResumeAnalysis(models.Model):
    """Store resume analysis results with full history"""
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='analyses')
    resume_url = models.CharField(max_length=500)
    
    # Extracted data
    extracted_skills = models.JSONField(default=list)  # List of skills
    experience_level = models.CharField(max_length=100, blank=True)
    
    # Analysis results
    strengths = models.JSONField(default=list)  # List of strength descriptions
    gaps = models.JSONField(default=list)  # List of areas for improvement
    summary = models.TextField(blank=True)  # AI-generated summary
    
    # Job matching
    job_matches = models.JSONField(default=dict)  # Matched jobs with scores
    recommendations_count = models.IntegerField(default=0)
    
    # Metadata
    processing_time = models.FloatField(null=True, blank=True)  # Time in seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Resume Analyses'
    
    def __str__(self):
        return f"{self.candidate.full_name} - Analysis on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
