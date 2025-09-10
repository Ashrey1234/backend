# # from .views import ResearcherProfileDetail
# from django.contrib.auth import views as auth_views
# from .views import ForgotPasswordView, ResetPasswordView
# from .views import CurrentUserView, DashboardStatsView


# from .views import MyTokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView

# # from .views import PaymentListCreateView, PaymentDetailView
# from . import views 

# from django.urls import path, include
# # from .views import UserFiveViewSet, UserBasicViewSet
# # from .views import UserFiveViewSet
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenBlacklistView,
# )
# from . import views

# router = DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'documents', views.DocumentViewSet)
# router.register(r'researcher-profiles', views.ResearcherProfileViewSet)
# # router.register(r'payments', views.PaymentViewSet)
# router.register(r'applications', views.ApplicationViewSet)
# router.register(r'attachments', views.AttachmentViewSet)
# router.register(r'notifications', views.NotificationViewSet)
# router.register(r'certificates', views.CertificateViewSet)








# urlpatterns = [
#     path('api/', include(router.urls)),
#     # Explicit endpoints for all main models
#     # path('api/applications/', views.ApplicationViewSet.as_view({'get': 'list'}), name='application-list'),
#     # path('api/applications/<int:pk>/', views.ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-detail'),
#     # path('api/attachments/', views.AttachmentViewSet.as_view({'get': 'list'}), name='attachment-list'),
#     # path('api/attachments/<int:pk>/', views.AttachmentViewSet.as_view({'get': 'retrieve'}), name='attachment-detail'),
#     path('api/certificates/', views.CertificateViewSet.as_view({'get': 'list'}), name='certificate-list'),
#     path('api/certificates/<int:pk>/', views.CertificateViewSet.as_view({'get': 'retrieve'}), name='certificate-detail'),
#     path('api/notifications/', views.NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
#     path('api/notifications/<int:pk>/', views.NotificationViewSet.as_view({'get': 'retrieve'}), name='notification-detail'),
   
#     path('api/researcher-profiles/', views.ResearcherProfileViewSet.as_view({'get': 'list'}), name='researcherprofile-list'),
#     path('api/researcher-profiles/<int:pk>/', views.ResearcherProfileViewSet.as_view({'get': 'retrieve'}), name='researcherprofile-detail'),
#     path('api/users/', views.UserViewSet.as_view({'get': 'list'}), name='user-list'),
#     path('api/users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
#     # Explicit document endpoints
#     path('api/documents/', views.DocumentViewSet.as_view({'get': 'list'}), name='document-list'),

#     # JWT Auth endpoints
#     path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

#     # Registration and custom endpointsvate
    
#     path('api/register/', views.RegisterView.as_view(), name='api-register'),
#     path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
#     path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),

#         # Custom endpoints for specific documents 
#     path('api/document/checklist/', views.DocumentChecklistView.as_view(), name='document-checklist'),
#     path('api/document/research-fee-structure/', views.DocumentResearchFeeStructureView.as_view(), name='document-research-fee-structure'),
#     path('api/document/zafiri-report-format/', views.DocumentZafiriReportFormatView.as_view(), name='document-zafiri-report-format'),
#     path('api/document/research-form/', views.DocumentResearchFormView.as_view(), name='document-research-form'),

#     path('api/document/research-proposal/', views.DocumentResearchProposalView.as_view(), name='document-research-proposal'),
     


#     # path('api/profile/', views.UserProfileView.as_view(), name='user-profile'),




#     path('api/password-reset/', ForgotPasswordView.as_view(), name='password-reset'),
#     path('api/password-reset-confirm/', ResetPasswordView.as_view(), name='password-reset-confirm'),



#     path('password-reset/', auth_views.PasswordResetView.as_view(
#         email_template_name='registration/password_reset_email.html',
#         success_url='/password-reset/done/',
#         subject_template_name='registration/password_reset_subject.txt',
#         extra_email_context={'frontend_url': 'http://localhost:5173/reset-password'}
#     ), name='password_reset'),
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
#         success_url='/reset/done/'
#     ), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),





#     path('api/payments/', views.payment_list, name='payment-list'),
#     path('api/payments/generate/', views.generate_payment, name='generate-payment'),


#     path('api/applications/', views.application_list, name='application-list'),
#     path('api/applications/<int:pk>/', views.application_detail, name='application-detail'),
#     path('api/applications/<int:pk>/submit/', views.application_submit, name='application-submit'),
#     path('api/applications/<int:pk>/approve/', views.application_approve, name='application-approve'),
#     path('api/applications/<int:pk>/reject/', views.application_reject, name='application-reject'),
#     path('api/applications/<int:application_pk>/attachments/', views.attachment_list, name='attachment-list'),
#     path('api/applications/<int:application_pk>/attachments/<int:pk>/', views.attachment_detail, name='attachment-detail'),

     
# ]




















from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from . import views
from .views import MyTokenObtainPairView, ForgotPasswordView, ResetPasswordView, CurrentUserView, DashboardStatsView

# Router for main ViewSets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'researcher-profiles', views.ResearcherProfileViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'certificates', views.CertificateViewSet)

urlpatterns = [
    # Router URLs
    path('api/', include(router.urls)),

    # Certificates (explicit endpoints for clarity)
    path('api/certificates/', views.CertificateViewSet.as_view({'get': 'list'}), name='certificate-list'),
    path('api/certificates/<int:pk>/', views.CertificateViewSet.as_view({'get': 'retrieve'}), name='certificate-detail'),

    # Notifications
    path('api/notifications/', views.NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    path('api/notifications/<int:pk>/', views.NotificationViewSet.as_view({'get': 'retrieve'}), name='notification-detail'),

    # Researcher profiles
    path('api/researcher-profiles/', views.ResearcherProfileViewSet.as_view({'get': 'list'}), name='researcherprofile-list'),
    path('api/researcher-profiles/<int:pk>/', views.ResearcherProfileViewSet.as_view({'get': 'retrieve'}), name='researcherprofile-detail'),

    # Users
    path('api/users/', views.UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('api/users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),

    # Documents
    path('api/documents/', views.DocumentViewSet.as_view({'get': 'list'}), name='document-list'),

    # JWT Auth endpoints
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # Registration and dashboard
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),

    # Custom document endpoints
    path('api/document/checklist/', views.DocumentChecklistView.as_view(), name='document-checklist'),
    path('api/document/research-fee-structure/', views.DocumentResearchFeeStructureView.as_view(), name='document-research-fee-structure'),
    path('api/document/zafiri-report-format/', views.DocumentZafiriReportFormatView.as_view(), name='document-zafiri-report-format'),
    path('api/document/research-form/', views.DocumentResearchFormView.as_view(), name='document-research-form'),
    path('api/document/research-proposal/', views.DocumentResearchProposalView.as_view(), name='document-research-proposal'),

    # Password reset
    path('api/password-reset/', ForgotPasswordView.as_view(), name='password-reset'),
    path('api/password-reset-confirm/', ResetPasswordView.as_view(), name='password-reset-confirm'),

    # Django built-in password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html',
        success_url='/password-reset/done/',
        subject_template_name='registration/password_reset_subject.txt',
        extra_email_context={'frontend_url': 'http://localhost:5173/reset-password'}
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Payments
    path('api/payments/', views.payment_list, name='payment-list'),
    path('api/payments/generate/', views.generate_payment, name='generate-payment'),

    # Applications and attachments
    path('api/applications/', views.application_list, name='application-list'),
    path('api/applications/<int:pk>/', views.application_detail, name='application-detail'),
    path('api/applications/<int:pk>/submit/', views.application_submit, name='application-submit'),
    path('api/applications/<int:pk>/approve/', views.application_approve, name='application-approve'),
    path('api/applications/<int:pk>/reject/', views.application_reject, name='application-reject'),
    path('api/applications/<int:application_pk>/attachments/', views.attachment_list, name='attachment-list'),
    path('api/applications/<int:application_pk>/attachments/<int:pk>/', views.attachment_detail, name='attachment-detail'),
]






