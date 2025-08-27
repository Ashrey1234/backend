from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ResearcherProfile, Payment, Application, Attachment, Notification, Certificate, Document
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'type', 'is_staff', 'is_superuser', 'is_active')
	list_filter = ('role', 'type', 'is_staff', 'is_superuser', 'is_active')
	search_fields = ('username', 'email', 'first_name', 'last_name', 'role', 'type')

	fieldsets = BaseUserAdmin.fieldsets + (
		('Custom Fields', {'fields': ('role', 'type', 'country')}),
	)
	add_fieldsets = BaseUserAdmin.add_fieldsets + (
		('Custom Fields', {'fields': ('role', 'type', 'country')}),
	)

@admin.register(ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
	pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	pass

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	pass

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
	pass

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	pass

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
	pass
