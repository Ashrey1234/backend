from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['request'] = self.request
		return context

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import serializers

class RegisterView(generics.CreateAPIView):
	queryset = get_user_model().objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

from rest_framework import viewsets
from .models import User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate
from .serializers import (
	UserSerializer, ResearcherProfileSerializer, PaymentSerializer, ApplicationSerializer,
	AttachmentSerializer, NotificationSerializer, CertificateSerializer
)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class ResearcherProfileViewSet(viewsets.ModelViewSet):
	queryset = ResearcherProfile.objects.all()
	serializer_class = ResearcherProfileSerializer

class PaymentViewSet(viewsets.ModelViewSet):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
	queryset = Application.objects.all()
	serializer_class = ApplicationSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
	queryset = Attachment.objects.all()
	serializer_class = AttachmentSerializer

class NotificationViewSet(viewsets.ModelViewSet):
	queryset = Notification.objects.all()
	serializer_class = NotificationSerializer

class CertificateViewSet(viewsets.ModelViewSet):
	queryset = Certificate.objects.all()
	serializer_class = CertificateSerializer





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Application, Payment

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Application, Payment

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
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

# class DashboardStatsView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         return Response({
#             "users": User.objects.count(),
#             "applications": Application.objects.count(),
#             "payments": Payment.objects.count(),
#         })


# filepath: /home/ashrey/Desktop/backendlastone/backend/myproject/myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Application, Payment

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            "applications": Application.objects.count(),
            "pending_applications": Application.objects.filter(status="Pending").count(),
            "payments": Payment.objects.filter(status="Verified").count(),
            "users": User.objects.count(),
        })



from rest_framework import viewsets
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer