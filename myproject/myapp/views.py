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





from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Payment, Application
from .serializers import PaymentSerializer, GeneratePaymentSerializer

# ----------------------------
# Create payment (full)
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    """
    Create a new payment for the authenticated user
    """
    try:
        data = request.data.copy()
        if 'expiry_date' not in data:
            data['expiry_date'] = timezone.now() + timedelta(days=180)

        serializer = PaymentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            payment = serializer.save(researcher=request.user)
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

# ----------------------------
# Create payment simple
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_simple(request):
    """
    Simple way to create payment - auto-fills category, level, nationality
    """
    try:
        serializer = GeneratePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        research_type = serializer.validated_data['research_type']
        year = serializer.validated_data['year']
        application_id = serializer.validated_data.get('application_id')

        application = None
        category = ''
        if application_id:
            try:
                application = Application.objects.get(id=application_id)
                category = application.category
            except Application.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Application not found'
                }, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            researcher=request.user,
            research_type=research_type,
            year=year,
            category=category,
            level=getattr(request.user, 'education_level', None),
            nationality=getattr(request.user, 'nationality', None),
            application=application,
            expiry_date=timezone.now() + timedelta(days=180)
        )

        response_serializer = PaymentSerializer(payment)
        return Response({
            'success': True,
            'message': 'Payment created successfully',
            'payment': response_serializer.data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error creating payment: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------
# Get all user payments
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_payments(request):
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

# ----------------------------
# Get payment detail
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_detail(request, payment_id):
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



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Application, Attachment
from .serializers import ApplicationSerializer, AttachmentSerializer


# ----------------------------
# Application Views
# ----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def application_list(request):
    if request.user.is_staff:
        applications = Application.objects.all()
    else:
        applications = Application.objects.filter(researcher=request.user)
    serializer = ApplicationSerializer(applications, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if not (request.user.is_staff or application.researcher == request.user):
        return Response({'error': 'Not allowed'}, status=403)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != application.researcher:
            return Response({'error': 'Only researcher can edit'}, status=403)
        serializer = ApplicationSerializer(application, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if request.user != application.researcher:
            return Response({'error': 'Only researcher can delete'}, status=403)
        application.delete()
        return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_submit(request, pk):
    application = get_object_or_404(Application, pk=pk, researcher=request.user)
    if application.status == 'Draft':
        application.status = 'Pending'
        application.submitted_at = timezone.now()
        application.save()
        return Response({'status': 'application submitted'})
    return Response({'error': 'Application already submitted'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_approve(request, pk):
    if not request.user.is_staff:
        return Response(status=403)
    application = get_object_or_404(Application, pk=pk)
    application.status = 'Approved'
    application.save()
    return Response({'status': f'Application approved for {application.researcher.username}'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def application_reject(request, pk):
    if not request.user.is_staff:
        return Response(status=403)
    application = get_object_or_404(Application, pk=pk)
    application.status = 'Rejected'
    application.officer_feedback = request.data.get('feedback', '')
    application.save()
    return Response({'status': f'Feedback sent to {application.researcher.username}'})


# ----------------------------
# Attachment Views
# ----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def attachment_list(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)

    if not (request.user.is_staff or application.researcher == request.user):
        return Response({'error': 'Not allowed'}, status=403)

    if request.method == 'GET':
        attachments = Attachment.objects.filter(application=application)
        serializer = AttachmentSerializer(attachments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user != application.researcher:
            return Response({'error': 'Only researcher can upload attachments'}, status=403)
        serializer = AttachmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(application=application, file_path=request.FILES.get('file_path'))
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def attachment_detail(request, application_pk, pk):
    application = get_object_or_404(Application, pk=application_pk)

    if not (request.user.is_staff or application.researcher == request.user):
        return Response({'error': 'Not allowed'}, status=403)

    attachment = get_object_or_404(Attachment, pk=pk, application=application)

    if request.method == 'GET':
        serializer = AttachmentSerializer(attachment, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != application.researcher:
            return Response({'error': 'Only researcher can update attachment'}, status=403)
        serializer = AttachmentSerializer(attachment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(file_path=request.FILES.get('file_path'))
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if request.user != application.researcher:
            return Response({'error': 'Only researcher can delete attachment'}, status=403)
        attachment.delete()
        return Response(status=204)















from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Certificate
from .serializers import CertificateSerializer
from django.utils import timezone

# ----------------------------
# Certificate Views
# ----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def certificate_list(request):
    """
    List all certificates (staff) or user's own (researcher) 
    / Create new certificate
    """
    if request.method == 'GET':
        if request.user.is_staff:
            certificates = Certificate.objects.all()
        else:
            certificates = Certificate.objects.filter(researcher=request.user)
        serializer = CertificateSerializer(certificates, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CertificateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Automatically set researcher to current user if not staff
            if not request.user.is_staff:
                serializer.save(researcher=request.user, issued_date=timezone.now())
            else:
                # Staff can set researcher manually
                serializer.save(issued_date=timezone.now())
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def certificate_detail(request, pk):
    """
    Retrieve, update, or delete a certificate
    """
    certificate = get_object_or_404(Certificate, pk=pk)

    # Permission: researcher can only access their own certificate
    if not request.user.is_staff and certificate.researcher != request.user:
        return Response({'error': 'Not allowed'}, status=403)

    if request.method == 'GET':
        serializer = CertificateSerializer(certificate, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CertificateSerializer(certificate, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        certificate.delete()
        return Response({'status': 'Certificate deleted'}, status=204)






# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Application

# views.py
from .models import Certificate
from django.utils import timezone



class ApplicationApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)

        if application.status != 'Pending':
            return Response({'error': 'Application cannot be approved'}, status=400)

        feedback = request.data.get('feedback', '')
        application.officer_feedback = feedback
        application.status = 'Approved'
        application.approved_at = timezone.now()
        application.save()

        # Generate Certificate
        certificate, created = Certificate.objects.get_or_create(
            application=application,
            defaults={
                'certificate_number': f"CERT-{application.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                'officer_feedback': feedback
            }
        )

        return Response({
            'success': True,
            'message': 'Application approved and certificate generated',
            'certificate': CertificateSerializer(certificate).data
        }, status=200)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from .models import Application
import os




from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from .models import Application
import os



# views.py
# class ApplicationCertificateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             application = Application.objects.get(pk=pk)
#         except Application.DoesNotExist:
#             raise Http404("Application not found")

#         if not hasattr(application, "certificate") or not application.certificate:
#             raise Http404("Certificate not generated yet")

#         cert = application.certificate
#         certificate_path = cert.file_path.path

#         if not os.path.exists(certificate_path):
#             raise Http404("Certificate file not found on server")

#         return FileResponse(
#             open(certificate_path, "rb"),
#             content_type="application/pdf",
#             as_attachment=True,
#             filename=os.path.basename(certificate_path)
#         )



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from .models import Application, Certificate
from .serializers import CertificateSerializer

class ApplicationCertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)

        if not hasattr(application, "certificate") or not application.certificate:
            raise Http404("Certificate not generated yet")

        cert = application.certificate

        if request.user.role == "Officer":
            if not cert.offline_file:
                raise Http404("Offline certificate not available")
            # Officer download offline copy
            return FileResponse(
                cert.offline_file.open("rb"),
                content_type="application/pdf",
                as_attachment=True,
                filename=f"certificate_officer_{cert.certificate_number}.pdf"
            )
        else:
            # Researcher online view
            serializer = CertificateSerializer(cert, context={"request": request})
            return Response(serializer.data)





# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from myapp.models import Application
from .serializers import ResearcherStatsSerializer

class ResearcherStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        researcher = request.user
        stats = {
            "total": Application.objects.filter(researcher=researcher).count(),
            "approved": Application.objects.filter(researcher=researcher, status='approved').count(),
            "pending": Application.objects.filter(researcher=researcher, status='pending').count(),
            "rejected": Application.objects.filter(researcher=researcher, status='rejected').count(),
        }

        serializer = ResearcherStatsSerializer(stats)
        return Response(serializer.data)




# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import UserSerializer

class ProfileDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)



    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update profile completion
            filled_fields = 0
            for field in ['username','email','phone_number','country','type','role','research_type','gender']:
                if getattr(user, field):
                    filled_fields += 1
            user.profile_completion = round(filled_fields / 8 * 100)
            user.save()

            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=400)






        # views.py
from django.shortcuts import render, get_object_or_404
from .models import Application

def verify_certificate(request, application_id):
    app = get_object_or_404(Application, id=application_id)
    certificate = getattr(app, "certificate", None)
    context = {
        "researcher": app.researcher.get_full_name() or app.researcher.username,
        "title": app.title,
        "feedback": app.officer_feedback or "(No feedback given)",
        "issued_date": certificate.issued_date.strftime("%Y-%m-%d") if certificate else "N/A"
    }
    return render(request, "verify_certificate.html", context)



















