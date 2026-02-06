from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, SubUserView, CustomTokenObtainPairView

urlpatterns = [
    path('signup', RegisterView.as_view(), name='auth_register_signup'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair_alias'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me', SubUserView.as_view(), name='auth_me'),
]
