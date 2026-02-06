from django.contrib import admin
from .models import Candidate, Application, Interview, Recommendation, ResumeAnalysis


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'email', 'user', 'experience_level', 'created_at')
	search_fields = ('full_name', 'email', 'user__username')
	readonly_fields = ('created_at', 'updated_at')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('candidate', 'job', 'status', 'source', 'applied_at')
	list_filter = ('status', 'source')
	search_fields = ('candidate__full_name', 'job__title')


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
	list_display = ('application', 'scheduled_time', 'status', 'result')
	list_filter = ('status', 'result')
	search_fields = ('application__candidate__full_name', 'application__job__title')


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
	list_display = ('job', 'candidate', 'match_score', 'created_at')
	search_fields = ('job__title', 'candidate__full_name')


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
	list_display = ('candidate', 'experience_level', 'created_at')
	search_fields = ('candidate__full_name',)
	readonly_fields = ('created_at',)
