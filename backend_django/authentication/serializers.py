from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name')

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'candidate'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # We allow either 'username' or 'email' from the frontend
        # and map it to USERNAME_FIELD
        username = attrs.get(self.username_field)
        if not username and 'email' in attrs:
            username = attrs['email']
            attrs[self.username_field] = username

        try:
            data = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            # Check if user exists but inactive
            user_exists = User.objects.filter(**{self.username_field: username}).exists()
            if user_exists:
                user = User.objects.get(**{self.username_field: username})
                if not user.is_active:
                    raise exceptions.AuthenticationFailed('This account is inactive.', code='user_inactive')
                raise exceptions.AuthenticationFailed('Incorrect password.', code='invalid_password')
            raise exceptions.AuthenticationFailed('No account found with this email.', code='user_not_found')

        # Add extra responses
        data['role'] = self.user.role
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        return data
