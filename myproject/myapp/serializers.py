
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    User, ResearcherProfile, Application, Attachment,
    Payment, Certificate, Notification, Document
)
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# ----------------------------
# User Serializers
# ----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'password', 'email', 'first_name', 'last_name',
            'role', 'type', 'country', 'research_type', 'phone_number'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'type', 'country', 'research_type', 'phone_number',
            'gender', 'profile_completion'
        ]



class UserProfileSerializer(serializers.ModelSerializer):
    researchInterests = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'name', 'email', 'institution', 'department', 'position',
            'contactNumber', 'researchInterests', 'bio', 'gender'
        ]

# JWT Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data

# ----------------------------
# Researcher Profile Serializer
# ----------------------------
class ResearcherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearcherProfile
        fields = [
            "id",
            "user",
            "name",
            "email",
            "institution",
            "department",
            "position",
            "contact_number",
            "gender",
            "research_interests",
            "bio",
        ]
        read_only_fields = ["user", "email"]

# ----------------------------
# Payment Serializer
# ----------------------------






import datetime
from rest_framework import serializers
from .models import Payment, Application

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('control_number', 'amount', 'expiry_date', 'generated_date', 'researcher')

class GeneratePaymentSerializer(serializers.Serializer):
    research_type = serializers.ChoiceField(choices=[
        ('Environment & Marine', 'Environment & Marine'),
        ('Aquatic Organisms', 'Aquatic Organisms'),
        ('Fisheries Research', 'Fisheries Research')
    ])
    year = serializers.IntegerField(
        min_value=2000,
        max_value=datetime.datetime.now().year + 5
    )
    application_id = serializers.IntegerField(required=False)








# ----------------------------
# Attachment Serializer
# ----------------------------
class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    original_filename = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id', 'file_type', 'original_filename', 'file_size',
            'file_url', 'uploaded_at', 'application',
        ]
        read_only_fields = ('application', 'uploaded_at', 'file_size')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file_path and request:
            return request.build_absolute_uri(obj.file_path.url)
        return None

    def get_original_filename(self, obj):
        return obj.original_filename or (
            obj.file_path.name.split('/')[-1] if obj.file_path else "unknown"
        )

# ----------------------------
# Application Serializer
# ----------------------------
class ApplicationSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    researcher_name = serializers.CharField(source='researcher.username', read_only=True)
    status = serializers.CharField(read_only=True)
    officer_feedback = serializers.CharField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'title', 'category', 'research_type', 'year',
            'start_date', 'end_date', 'description',
            'objectives', 'methodology', 'expected_outcomes',
            'status', 'officer_feedback', 'researcher_name',
            'attachments', 'created_at', 'updated_at', 'submitted_at'
        ]
        read_only_fields = (
            'researcher_name', 'status', 'officer_feedback',
            'created_at', 'updated_at', 'submitted_at'
        )

    def create(self, validated_data):
        validated_data['researcher'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] == 'Pending':
            validated_data['submitted_at'] = timezone.now()
        return super().update(instance, validated_data)

    def validate(self, data):
        start_date = data.get('start_date') or getattr(self.instance, 'start_date', None)
        end_date = data.get('end_date') or getattr(self.instance, 'end_date', None)

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date cannot be earlier than start date.")

        if data.get('status') == 'Pending':
            if not data.get('objectives') and not getattr(self.instance, 'objectives', None):
                raise serializers.ValidationError("Objectives are required before submitting.")
            if not data.get('expected_outcomes') and not getattr(self.instance, 'expected_outcomes', None):
                raise serializers.ValidationError("Expected outcomes are required before submitting.")
        return data



# serializers.py
# from rest_framework import serializers
# from .models import Certificate

# class CertificateSerializer(serializers.ModelSerializer):
#     officer_feedback = serializers.CharField(read_only=True)  # 🔹Include this

#     class Meta:
#         model = Certificate
#         fields = ['id', 'application', 'certificate_number', 'file_path', 'issued_date', 'officer_feedback']

from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'certificate_number', 'file_path', 'offline_file', 'issued_date', 'officer_feedback']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if request and hasattr(request.user, "role"):
            if request.user.role == "Officer":
                # Officer apewe offline_file pekee
                data.pop("file_path", None)
            else:
                # Researcher apewe online copy pekee
                data.pop("offline_file", None)

        return data




# ----------------------------
# Notification Serializer
# ----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'status', 'created_at']

# ----------------------------
# Document Serializer
# ----------------------------
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'uploaded_at', 'file', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None







# serializers.py
from rest_framework import serializers

class ResearcherStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    approved = serializers.IntegerField()
    pending = serializers.IntegerField()
    rejected = serializers.IntegerField()










from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserSerializer

class ProfileDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



