from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, Company
from .serializers import JobSerializer, CompanySerializer

class IsRecruiterOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'recruiter'

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Auto-assign company if recruiter has one
        company = self.request.user.companies.first()
        if company:
            serializer.save(company=company)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                "error": "You must have a company profile before posting a job. Please go to Company Settings."
            })

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsRecruiterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobMatchScoreView(APIView):
    """Calculate match score between candidate and job"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, job_id):
        from candidates.models import Candidate
        import json
        
        try:
            job = Job.objects.get(id=job_id)
            
            # Get candidate profile
            try:
                candidate = Candidate.objects.get(user=request.user)
            except Candidate.DoesNotExist:
                return Response({
                    "match_score": 0,
                    "message": "Please upload your resume first to see match scores",
                    "matched_skills": [],
                    "missing_skills": [],
                    "has_resume": False
                }, status=status.HTTP_200_OK)
            
            # Get candidate skills from analysis report
            candidate_skills = set()
            if candidate.analysis_report and isinstance(candidate.analysis_report, dict):
                skills_data = candidate.analysis_report.get('skills', [])
                if isinstance(skills_data, list):
                    candidate_skills = set([s.lower() for s in skills_data])
            
            # Get job requirements
            job_requirements = job.requirements
            if isinstance(job_requirements, str):
                try:
                    job_requirements = json.loads(job_requirements)
                except:
                    job_requirements = []
            
            if not isinstance(job_requirements, list):
                job_requirements = []
            
            job_skills = set([r.lower() for r in job_requirements])
            
            # Calculate match
            if not job_skills:
                match_score = 0
                matched_skills = []
                missing_skills = []
            else:
                matched_skills = list(candidate_skills.intersection(job_skills))
                missing_skills = list(job_skills - candidate_skills)
                match_score = int((len(matched_skills) / len(job_skills)) * 100)
            
            # Get strengths and gaps from analysis
            strengths = []
            gaps = []
            if candidate.analysis_report and isinstance(candidate.analysis_report, dict):
                analysis_results = candidate.analysis_report.get('analysis_results', {})
                if isinstance(analysis_results, dict):
                    strengths = analysis_results.get('strengths', [])
                    gaps = analysis_results.get('gaps', [])
            
            return Response({
                "match_score": match_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "strengths": strengths[:3],  # Top 3 strengths
                "gaps": gaps[:3],  # Top 3 gaps
                "has_resume": True
            }, status=status.HTTP_200_OK)
            
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
