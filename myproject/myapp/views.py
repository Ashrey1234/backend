from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserProfileSerializer

# User profile API view
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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



from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Payment
from .serializers import PaymentSerializer, GeneratePaymentSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_list(request):
    payments = Payment.objects.filter(researcher=request.user).order_by('-generated_date')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def generate_payment(request):
    serializer = GeneratePaymentSerializer(data=request.data)
    if serializer.is_valid():
        expiry_date = timezone.now() + timedelta(days=30)
        payment = Payment(
            researcher=request.user,
            research_type=serializer.validated_data['research_type'],
            year=serializer.validated_data['year'],
            status='Pending',
            expiry_date=expiry_date,
            amount=100000
        )
        payment.save()
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










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





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

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
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": getattr(user, "phone_number", None),
            "research_type": getattr(user, "research_type", None),
        })


















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

# Custom document serving views
from django.http import FileResponse, Http404
import os
from django.conf import settings

class DocumentChecklistDOSylgrView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/checklist_DOSylgr.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class DocumentChecklistView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/checklist.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class DocumentResearchFeeStructureView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/Research_Fee_Structure.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class DocumentZafiriReportFormatView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/zafiri_report_format.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class DocumentResearchFormView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/reserchForm.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

class DocumentResearchProposalView(APIView):
    permission_classes = []
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'media/documents/zafiri_RESEARCH_PROPOSALA.pdf')
        if not os.path.exists(file_path):
            raise Http404
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')






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











from rest_framework import generics, permissions
from .models import ResearcherProfile
from .serializers import ResearcherProfileSerializer

# View ya kupata profile ya currently logged-in researcher
class ResearcherProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ResearcherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Hii inarudisha profile ya currently logged-in user
        return self.request.user.researcher_profile















from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer






# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Payment
from .serializers import PaymentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    """
    Create a new payment for the authenticated user
    """
    try:
        # Add default expiry date if not provided (6 months from now)
        data = request.data.copy()
        if 'expiry_date' not in data:
            data['expiry_date'] = timezone.now() + timedelta(days=180)
        
        # Create serializer with request context
        serializer = PaymentSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            payment = serializer.save()
            
            # Return created payment data
            response_serializer = PaymentSerializer(payment)
            return Response({
                'success': True,
                'message': 'Payment created successfully',
                'payment': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error creating payment: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_payments(request):
    """
    Get all payments for the authenticated user
    """
    try:
        payments = Payment.objects.filter(researcher=request.user).order_by('-generated_date')
        serializer = PaymentSerializer(payments, many=True)
        
        return Response({
            'success': True,
            'payments': serializer.data,
            'total_payments': payments.count()
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error fetching payments: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_detail(request, payment_id):
    """
    Get specific payment details (only if it belongs to the user)
    """
    try:
        payment = Payment.objects.get(id=payment_id, researcher=request.user)
        serializer = PaymentSerializer(payment)
        
        return Response({
            'success': True,
            'payment': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Payment.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Payment not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error fetching payment: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_simple(request):
    """
    Simple way to create payment - just provide research_type and year
    """
    try:
        research_type = request.data.get('research_type', 'Environment & Marine')
        year = request.data.get('year', timezone.now().year)
        
        # Create payment directly
        payment = Payment.objects.create(
            researcher=request.user,  # Automatically set to current user
            research_type=research_type,
            year=year,
            expiry_date=timezone.now() + timedelta(days=180)
            # amount na control_number zitaundwa automatic katika save() method
        )
        
        # Return payment data
        serializer = PaymentSerializer(payment)
        return Response({
            'success': True,
            'message': 'Payment created successfully',
            'payment': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error creating payment: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









