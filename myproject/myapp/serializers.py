from .models import Document
from rest_framework import serializers
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at']

from rest_framework import serializers
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role', 'type', 'country']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
from rest_framework import serializers
from .models import User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'type', 'country', 'is_active', 'is_staff', 'is_superuser']

class ResearcherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearcherProfile
        fields = ['id', 'researcher', 'institution', 'contact', 'system_id']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'researcher', 'research_type', 'control_number', 'amount', 'status', 'generated_date', 'expiry_date']
        read_only_fields = ['control_number', 'amount']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'researcher', 'title', 'category', 'start_date', 'end_date', 'status', 'officer_feedback']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'application', 'file_type', 'file_path']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'status', 'created_at']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'application', 'certificate_number', 'file_path', 'issued_date']
