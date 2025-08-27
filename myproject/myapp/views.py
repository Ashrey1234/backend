from rest_framework import viewsets
from .models import Document
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer

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
