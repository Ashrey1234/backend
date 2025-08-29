from .views import CurrentUserView, DashboardStatsView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'researcher-profiles', views.ResearcherProfileViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'applications', views.ApplicationViewSet)
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'certificates', views.CertificateViewSet)

from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('api/', include(router.urls)),
    # Explicit endpoints for all main models
    path('api/applications/', views.ApplicationViewSet.as_view({'get': 'list'}), name='application-list'),
    path('api/applications/<int:pk>/', views.ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-detail'),
    path('api/attachments/', views.AttachmentViewSet.as_view({'get': 'list'}), name='attachment-list'),
    path('api/attachments/<int:pk>/', views.AttachmentViewSet.as_view({'get': 'retrieve'}), name='attachment-detail'),
    path('api/certificates/', views.CertificateViewSet.as_view({'get': 'list'}), name='certificate-list'),
    path('api/certificates/<int:pk>/', views.CertificateViewSet.as_view({'get': 'retrieve'}), name='certificate-detail'),
    path('api/notifications/', views.NotificationViewSet.as_view({'get': 'list'}), name='notification-list'),
    path('api/notifications/<int:pk>/', views.NotificationViewSet.as_view({'get': 'retrieve'}), name='notification-detail'),
    path('api/payments/', views.PaymentViewSet.as_view({'get': 'list'}), name='payment-list'),
    path('api/payments/<int:pk>/', views.PaymentViewSet.as_view({'get': 'retrieve'}), name='payment-detail'),
    path('api/researcher-profiles/', views.ResearcherProfileViewSet.as_view({'get': 'list'}), name='researcherprofile-list'),
    path('api/researcher-profiles/<int:pk>/', views.ResearcherProfileViewSet.as_view({'get': 'retrieve'}), name='researcherprofile-detail'),
    path('api/users/', views.UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('api/users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    # Explicit document endpoints
    path('api/documents/', views.DocumentViewSet.as_view({'get': 'list'}), name='document-list'),
    path('api/documents/<int:pk>/', views.DocumentViewSet.as_view({'get': 'retrieve'}), name='document-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),




    path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('api/dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]


