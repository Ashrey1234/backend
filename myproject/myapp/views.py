from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import (
    User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate, Document
)
from .serializers import (
    UserSerializer, RegisterSerializer, ResearcherProfileSerializer, PaymentSerializer,
    ApplicationSerializer, AttachmentSerializer, NotificationSerializer, CertificateSerializer,
    DocumentSerializer
)

# Document ViewSet
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# Register View
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ResearcherProfile ViewSet
class ResearcherProfileViewSet(viewsets.ModelViewSet):
    queryset = ResearcherProfile.objects.all()
    serializer_class = ResearcherProfileSerializer

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Application ViewSet
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

# Attachment ViewSet
class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# Certificate ViewSet
class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

# Current User API
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": getattr(user, "role", None),
            "type": getattr(user, "type", None),
            "country": getattr(user, "country", None),
        })

# Dashboard Stats API
# class DashboardStatsView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         return Response({
#             "applications": Application.objects.count(),
#             "pending_applications": Application.objects.filter(status="Pending").count(),
#             "payments": Payment.objects.filter(status="Verified").count(),
#             "users": User.objects.count(),
#         })






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Application, Payment, User

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status='Pending').count()
        verified_payments = Payment.objects.filter(status='Verified').count()
        total_users = User.objects.count()
        return Response({
            "applications": total_applications,
            "pending_applications": pending_applications,
            "payments": verified_payments,
            "users": total_users,
        })





# class DashboardStatsView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         applications_count = Application.objects.count()
#         pending_count = Application.objects.filter(status__iexact="Pending").count()  
#         payments_count = Payment.objects.filter(status__iexact="Verified").count()    
#         users_count = User.objects.count()

#         return Response({
#             "applications": applications_count,
#             "pending_applications": pending_count,
#             "payments": payments_count,
#             "users": users_count,
#         })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .models import User

class ForgotPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "If an account exists with this email, you will receive a password reset link shortly."}, status=status.HTTP_200_OK)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return Response({"message": "If an account exists with this email, you will receive a password reset link shortly."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        if not uidb64 or not token or not password:
            return Response({"error": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

from rest_framework import generics
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer      