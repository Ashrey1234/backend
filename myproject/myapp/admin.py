from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Payment, Application, Attachment, Notification, Certificate, Document, ResearcherProfile
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







from django.contrib import admin
from .models import ResearcherProfile

@admin.register(ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'position', 'institution')  # customize fields to show
    search_fields = ('user__username', 'user__email', 'department', 'position', 'institution')
    list_filter = ('department', 'institution')











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

