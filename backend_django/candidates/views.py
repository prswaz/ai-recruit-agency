from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Candidate, Application, Interview, Recommendation, ResumeAnalysis
from core.models import Skill, Job
from .serializers import (
    CandidateSerializer, ApplicationSerializer, 
    InterviewSerializer, RecommendationSerializer,
    ResumeAnalysisSerializer
)

class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get profile for current user, create if not exists
        obj, created = Candidate.objects.get_or_create(
            user=self.request.user,
            defaults={'full_name': f"{self.request.user.first_name} {self.request.user.last_name}", 'email': self.request.user.email}
        )
        return obj

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Application.objects.filter(candidate__user=user).order_by('-applied_at')
        elif user.role == 'recruiter':
            # Applications for jobs owned by recruiter's companies
            return Application.objects.filter(job__company__user=user).order_by('-applied_at')
        return Application.objects.none()

    def perform_create(self, serializer):
        # Auto-link candidate
        candidate = self.request.user.candidate_profile.first()
        serializer.save(candidate=candidate)

class InterviewViewSet(viewsets.ReadOnlyModelViewSet):
    # Only read for now, schedule logic might be specific action
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Interview.objects.filter(application__candidate__user=user).order_by('-scheduled_time')
        # Recruiter logic...
        return Interview.objects.none()

class RecommendationListView(generics.ListAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Recommendation.objects.filter(candidate__user=user).order_by('-match_score')
        return Recommendation.objects.none()

class ResumeAnalysisListView(generics.ListAPIView):
    serializer_class = ResumeAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(candidate__user=self.request.user).order_by('-created_at')

from .services import ResumeAnalysisService
from asgiref.sync import async_to_sync

class AIResumeAnalyzeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No resume file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        resume_file = request.FILES['file']
        
        try:
            # Call service to handle extraction, analysis, persistence and recommendations
            # Use async_to_sync to run async service from sync view context
            result = async_to_sync(ResumeAnalysisService.process_resume_upload)(request.user, resume_file)

            return Response({
                "status": "success",
                "message": "Resume analyzed successfully",
                "data": result['report'],
                "metadata": {
                    "skills_detected": result['skills_count'],
                    "resume_url": result['candidate'].resume_url
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                "status": "error",
                "message": f"AI Processing failed: {str(e)}",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CandidateLatestAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            candidate = request.user.candidate_profile.first()
            if not candidate:
                return Response({"error": "Candidate profile not found"}, status=404)
            
            latest_analysis = ResumeAnalysis.objects.filter(candidate=candidate).first()
            if not latest_analysis:
                return Response({
                    "has_analysis": False,
                    "message": "No analysis found for this candidate"
                })
            
            serializer = ResumeAnalysisSerializer(latest_analysis)
            return Response({
                "has_analysis": True,
                "data": serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
