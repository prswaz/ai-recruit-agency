import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_recruiter_django.settings')
django.setup()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
print(f"User Model: {User}")
print(f"USERNAME_FIELD: {User.USERNAME_FIELD}")

serializer = TokenObtainPairSerializer()
print("Serializer Fields:", serializer.fields.keys())
