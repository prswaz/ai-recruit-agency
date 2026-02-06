from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CandidateProfileView, ApplicationViewSet, 
    InterviewViewSet, RecommendationListView, AIResumeAnalyzeView,
    ResumeAnalysisListView, CandidateLatestAnalysisView
)

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='applications')
router.register(r'interviews', InterviewViewSet, basename='interviews')

urlpatterns = [
    path('me', CandidateProfileView.as_view(), name='candidate_profile'),
    path('profile/analysis', CandidateLatestAnalysisView.as_view(), name='candidate_latest_analysis'),
    path('resume/analyze', AIResumeAnalyzeView.as_view(), name='resume_analyze'),
    path('analysis-history/', ResumeAnalysisListView.as_view(), name='analysis-history'),
    path('recommendations/', RecommendationListView.as_view(), name='recommendations'),
    path('', include(router.urls)),
]
