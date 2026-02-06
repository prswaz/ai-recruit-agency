from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, CompanyViewSet, JobMatchScoreView

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('jobs/<int:job_id>/match/', JobMatchScoreView.as_view(), name='job-match-score'),
]
