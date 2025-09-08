from .models import Document
from rest_framework import serializers
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'uploaded_at', 'file', 'file_url']  # add file_url

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url) if request else obj.file.url
        return None

from rest_framework import serializers
from django.contrib.auth import get_user_model

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

class UserProfileSerializer(serializers.ModelSerializer):
    researchInterests = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'name', 'email', 'institution', 'department', 'position',
            'contactNumber', 'researchInterests', 'bio', 'gender'
        ]
from .models import User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate











from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'type', 'country', 'is_active', 'is_staff', 'is_superuser',
            'research_type', 'phone_number'
        ]





from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Hapa tunarudisha role moja kwa moja
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data



















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
    applicant_name = serializers.CharField(source='researcher.get_full_name', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'researcher', 'applicant_name', 'title', 'category',
            'start_date', 'end_date', 'status', 'officer_feedback',
            'submitted', 'important'
        ]







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








from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'type', 'country', 'research_type', 'phone_number', 'role'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

















from rest_framework import serializers
from .models import ResearcherProfile

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
        read_only_fields = ["user", "email"]  # user na email zisiwezi kubadilishwa










from rest_framework import serializers
from .models import Payment
import datetime

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
