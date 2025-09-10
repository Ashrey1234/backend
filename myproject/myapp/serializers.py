# from .models import Document
# from rest_framework import serializers
# class DocumentSerializer(serializers.ModelSerializer):
#     file_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Document
#         fields = ['id', 'title', 'uploaded_at', 'file', 'file_url']  # add file_url

#     def get_file_url(self, obj):
#         request = self.context.get('request')
#         if obj.file and hasattr(obj.file, 'url'):
#             return request.build_absolute_uri(obj.file.url) if request else obj.file.url
#         return None

# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = [
#             'id', 'username', 'password', 'email', 'first_name', 'last_name',
#             'role', 'type', 'country', 'research_type', 'phone_number'
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = get_user_model().objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

# class UserProfileSerializer(serializers.ModelSerializer):
#     researchInterests = serializers.ListField(child=serializers.CharField(), required=False)

#     class Meta:
#         model = get_user_model()
#         fields = [
#             'name', 'email', 'institution', 'department', 'position',
#             'contactNumber', 'researchInterests', 'bio', 'gender'
#         ]
# from .models import User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate











# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'id', 'username', 'email', 'first_name', 'last_name',
#             'role', 'type', 'country', 'is_active', 'is_staff', 'is_superuser',
#             'research_type', 'phone_number'
#         ]





# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['role'] = user.role
#         return token

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # Hapa tunarudisha role moja kwa moja
#         data['role'] = self.user.role
#         data['username'] = self.user.username
#         return data



















# class ResearcherProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ResearcherProfile
#         fields = ['id', 'researcher', 'institution', 'contact', 'system_id']

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = ['id', 'researcher', 'research_type', 'control_number', 'amount', 'status', 'generated_date', 'expiry_date']
#         read_only_fields = ['control_number', 'amount']




# class ApplicationSerializer(serializers.ModelSerializer):
#     applicant_name = serializers.CharField(source='researcher.get_full_name', read_only=True)

#     class Meta:
#         model = Application
#         fields = [
#             'id', 'researcher', 'applicant_name', 'title', 'category',
#             'start_date', 'end_date', 'status', 'officer_feedback',
#             'important'
#         ]
# # 'submitted', 






# class AttachmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attachment
#         fields = ['id', 'application', 'file_type', 'file_path']

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'message', 'status', 'created_at']

# class CertificateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Certificate
#         fields = ['id', 'application', 'certificate_number', 'file_path', 'issued_date']








# from rest_framework import serializers
# from .models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'username', 'email', 'password', 'first_name', 'last_name',
#             'type', 'country', 'research_type', 'phone_number', 'role'
#         ]
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User.objects.create_user(password=password, **validated_data)
#         return user

















# from rest_framework import serializers
# from .models import ResearcherProfile

# class ResearcherProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ResearcherProfile
#         fields = [
#             "id",
#             "user",
#             "name",
#             "email",
#             "institution",
#             "department",
#             "position",
#             "contact_number",
#             "gender",
#             "research_interests",
#             "bio",
#         ]
#         read_only_fields = ["user", "email"]  # user na email zisiwezi kubadilishwa










# from rest_framework import serializers     
# from .models import Payment
# import datetime

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'
#         read_only_fields = ('control_number', 'amount', 'expiry_date', 'generated_date', 'researcher')



# class GeneratePaymentSerializer(serializers.Serializer):
#     research_type = serializers.ChoiceField(choices=[
#         ('Environment & Marine', 'Environment & Marine'),
#         ('Aquatic Organisms', 'Aquatic Organisms'),
#         ('Fisheries Research', 'Fisheries Research')
#     ])
    
#     year = serializers.IntegerField(
#         min_value=2000, 
#         max_value=datetime.datetime.now().year + 5
#     )












# # # ----------------------------                   now
# # # Serializers
# # # ----------------------------
# # from rest_framework import serializers
# # from .models import Application, Attachment

# # class AttachmentSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Attachment
# #         fields = '__all__'
# #         read_only_fields = ('application', 'uploaded_at', 'original_filename', 'file_size')

# # class ApplicationSerializer(serializers.ModelSerializer):
# #     attachments = AttachmentSerializer(many=True, read_only=True)
# #     status = serializers.CharField(read_only=True)  # Status changes should be handled by officers
# #     officer_feedback = serializers.CharField(read_only=True)  # Only officers can set feedback

# #     class Meta:
# #         model = Application
# #         fields = '__all__'
# #         read_only_fields = ('researcher', 'created_at', 'updated_at', 'submitted_at')

# #     def create(self, validated_data):
# #         # Set the current user as researcher
# #         validated_data['researcher'] = self.context['request'].user
# #         return super().create(validated_data)

# #     def update(self, instance, validated_data):
# #         # Handle submission timestamp
# #         if 'status' in validated_data and validated_data['status'] == 'Pending':
# #             validated_data['submitted_at'] = timezone.now()
# #         return super().update(instance, validated_data)













# # from rest_framework import serializers   earlie
# # from django.utils import timezone
# # from .models import Application, Attachment

# # # ----------------------------
# # # Attachment Serializer
# # # ----------------------------
# # class AttachmentSerializer(serializers.ModelSerializer):
# #     file_url = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Attachment
# #         fields = ['id', 'file_type', 'original_filename', 'file_size', 'file_url']
# #         read_only_fields = ('application', 'uploaded_at', 'original_filename', 'file_size')

# #     def get_file_url(self, obj):
# #         request = self.context.get('request')
# #         if obj.file_path and request:
# #             return request.build_absolute_uri(obj.file_path.url)
# #         return None


# # from rest_framework import serializers    asubuhi
# # from .models import Attachment

# # class AttachmentSerializer(serializers.ModelSerializer):
# #     file_url = serializers.SerializerMethodField()
# #     original_filename = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Attachment
# #         fields = ['id', 'file_type', 'original_filename', 'file_size', 'file_url']
# #         # read_only_fields = ('application', 'uploaded_at', 'file_size')

# #     def get_file_url(self, obj):
# #         request = self.context.get('request')
# #         if obj.file_path and request:
# #             return request.build_absolute_uri(obj.file_path.url)
# #         return None

# #     def get_original_filename(self, obj):
# #         return obj.original_filename or (obj.file_path.name.split('/')[-1] if obj.file_path else "unknown")



# # from rest_framework import serializers     kubali
# # from .models import Attachment

# # class AttachmentSerializer(serializers.ModelSerializer):
# #     file_url = serializers.SerializerMethodField()
# #     original_filename = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Attachment
# #         fields = [
# #             'id',
# #             'file_type',
# #             'original_filename',
# #             'file_size',
# #             'file_url',
# #             'uploaded_at',
# #             'application',
# #         ]
# #         read_only_fields = ('application', 'uploaded_at', 'file_size')

# #     def get_file_url(self, obj):
# #         request = self.context.get('request')
# #         if obj.file_path and request:
# #             return request.build_absolute_uri(obj.file_path.url)
# #         return None

# #     def get_original_filename(self, obj):
# #         return obj.original_filename or (
# #             obj.file_path.name.split('/')[-1] if obj.file_path else "unknown"
# #         )









# # # serializers.py                                             asubuhi
# # from rest_framework import serializers
# # from django.utils import timezone
# # from .models import Application, Attachment



# # from rest_framework import viewsets
# # from .models import Application
# # from .serializers import ApplicationSerializer

# # class ApplicationViewSet(viewsets.ModelViewSet):
# #     queryset = Application.objects.all()
# #     serializer_class = ApplicationSerializer

# #     def get_serializer_context(self):
# #         # Hii inahakikisha request ipo kwenye serializer
# #         context = super().get_serializer_context()
# #         context.update({"request": self.request})
# #         return context




# # # ----------------------------
# # # Application Serializer
# # # ----------------------------
# # class ApplicationSerializer(serializers.ModelSerializer):
# #     attachments = AttachmentSerializer(many=True, read_only=True)
# #     status = serializers.CharField(read_only=True)  # Officers handle status
# #     officer_feedback = serializers.CharField(read_only=True)  # Officers set feedback
# #     researcher_name = serializers.CharField(source='researcher.username', read_only=True)

# #     class Meta:
# #         model = Application
# #         fields = '__all__'
# #         read_only_fields = ('researcher', 'created_at', 'updated_at', 'submitted_at')

# #     def create(self, validated_data):
# #         # Set current user as researcher
# #         validated_data['researcher'] = self.context['request'].user
# #         return super().create(validated_data)

# #     def update(self, instance, validated_data):
# #         # Automatically set submitted_at if status is being set to Pending
# #         if 'status' in validated_data and validated_data['status'] == 'Pending':
# #             validated_data['submitted_at'] = timezone.now()
# #         return super().update(instance, validated_data)





















# # from rest_framework import serializers     asubuhi
# # from django.utils import timezone
# # from .models import Application, Attachment


# # class AttachmentSerializer(serializers.ModelSerializer):
# #     file_url = serializers.SerializerMethodField()
# #     original_filename = serializers.SerializerMethodField()

# #     class Meta:
# #         model = Attachment
# #         fields = [
# #             'id', 'file_type', 'original_filename', 'file_size',
# #             'file_url', 'uploaded_at', 'application',
# #         ]
# #         read_only_fields = ('application', 'uploaded_at', 'file_size')

# #     def get_file_url(self, obj):
# #         request = self.context.get('request')
# #         if obj.file_path and request:
# #             return request.build_absolute_uri(obj.file_path.url)
# #         return None

# #     def get_original_filename(self, obj):
# #         return obj.original_filename or (
# #             obj.file_path.name.split('/')[-1] if obj.file_path else "unknown"
# #         )


# # class ApplicationSerializer(serializers.ModelSerializer):
# #     attachments = AttachmentSerializer(many=True, read_only=True)
# #     status = serializers.CharField(read_only=True)
# #     officer_feedback = serializers.CharField(read_only=True)
# #     researcher_name = serializers.CharField(source='researcher.username', read_only=True)

# #     class Meta:
# #         model = Application
# #         fields = '__all__'
# #         read_only_fields = ('researcher', 'created_at', 'updated_at', 'submitted_at')

# #     def create(self, validated_data):
# #         validated_data['researcher'] = self.context['request'].user
# #         return super().create(validated_data)

# #     def update(self, instance, validated_data):
# #         if 'status' in validated_data and validated_data['status'] == 'Pending':
# #             validated_data['submitted_at'] = timezone.now()
# #         return super().update(instance, validated_data)
















# from rest_framework import serializers
# from django.utils import timezone
# from .models import Application, Attachment


# # --------------------------
# # Attachment Serializer
# # --------------------------
# class AttachmentSerializer(serializers.ModelSerializer):
#     file_url = serializers.SerializerMethodField()
#     original_filename = serializers.SerializerMethodField()

#     class Meta:
#         model = Attachment
#         fields = [
#             'id', 'file_type', 'original_filename', 'file_size',
#             'file_url', 'uploaded_at', 'application',
#         ]
#         read_only_fields = ('application', 'uploaded_at', 'file_size')

#     def get_file_url(self, obj):
#         request = self.context.get('request')
#         if obj.file_path and request:
#             return request.build_absolute_uri(obj.file_path.url)
#         return None

#     def get_original_filename(self, obj):
#         return obj.original_filename or (
#             obj.file_path.name.split('/')[-1] if obj.file_path else "unknown"
#         )


# # --------------------------
# # Application Serializer
# # --------------------------
# class ApplicationSerializer(serializers.ModelSerializer):
#     attachments = AttachmentSerializer(many=True, read_only=True)
#     researcher_name = serializers.CharField(source='researcher.username', read_only=True)
#     status = serializers.CharField(read_only=True)
#     officer_feedback = serializers.CharField(read_only=True)

#     class Meta:
#         model = Application
#         fields = [
#             'id', 'title', 'category', 'research_type', 'year',
#             'start_date', 'end_date', 'description',
#             'objectives', 'methodology', 'expected_outcomes',
#             'status', 'officer_feedback', 'researcher_name',
#             'attachments', 'created_at', 'updated_at', 'submitted_at'
#         ]
#         read_only_fields = (
#             'researcher_name', 'status', 'officer_feedback',
#             'created_at', 'updated_at', 'submitted_at'
#         )

#     def create(self, validated_data):
#         validated_data['researcher'] = self.context['request'].user
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         # Auto-set submitted_at when status changes to Pending
#         if 'status' in validated_data and validated_data['status'] == 'Pending':
#             validated_data['submitted_at'] = timezone.now()
#         return super().update(instance, validated_data)

#     def validate(self, data):
#         """
#         Custom validation:
#         - Ensure end_date is not earlier than start_date.
#         - Ensure objectives and expected_outcomes are not empty when submitting.
#         """
#         start_date = data.get('start_date') or getattr(self.instance, 'start_date', None)
#         end_date = data.get('end_date') or getattr(self.instance, 'end_date', None)

#         if start_date and end_date and end_date < start_date:
#             raise serializers.ValidationError("End date cannot be earlier than start date.")

#         if data.get('status') == 'Pending':
#             if not data.get('objectives') and not getattr(self.instance, 'objectives', None):
#                 raise serializers.ValidationError("Objectives are required before submitting.")
#             if not data.get('expected_outcomes') and not getattr(self.instance, 'expected_outcomes', None):
#                 raise serializers.ValidationError("Expected outcomes are required before submitting.")

#         return data





























































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
            'role', 'type', 'country', 'is_active', 'is_staff', 'is_superuser',
            'research_type', 'phone_number'
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

# ----------------------------
# Certificate Serializer
# ----------------------------
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'application', 'certificate_number', 'file_path', 'issued_date']

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
