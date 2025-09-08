# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, Payment, Application, Attachment, Notification, Certificate, Document, ResearcherProfile
# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
# 	pass

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
# 	list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'type', 'is_staff', 'is_superuser', 'is_active')
# 	list_filter = ('role', 'type', 'is_staff', 'is_superuser', 'is_active')
# 	search_fields = ('username', 'email', 'first_name', 'last_name', 'role', 'type')

# 	fieldsets = BaseUserAdmin.fieldsets + (
# 		('Custom Fields', {'fields': ('role', 'type', 'country')}),
# 	)
# 	add_fieldsets = BaseUserAdmin.add_fieldsets + (
# 		('Custom Fields', {'fields': ('role', 'type', 'country')}),
# 	)




# from django.contrib import admin
# from .models import ResearcherProfile

# @admin.register(ResearcherProfile)
# class ResearcherProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'department', 'position', 'institution')  # customize fields to show
#     search_fields = ('user__username', 'user__email', 'department', 'position', 'institution')
#     list_filter = ('department', 'institution')




# @admin.register(Payment) 
# class PaymentAdmin(admin.ModelAdmin):
# 	pass


# # @admin.register(Application)
# # class ApplicationAdmin(admin.ModelAdmin):
# # 	pass





# @admin.register(Application)
# class ApplicationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status', 'officer_feedback', 'submitted_at')  # use submitted_at instead of submitted


# @admin.register(Attachment)
# class AttachmentAdmin(admin.ModelAdmin):
# 	pass

# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
# 	pass

# @admin.register(Certificate)
# class CertificateAdmin(admin.ModelAdmin):
# 	pass





































from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import (
    User, Payment, Application, Attachment,
    Notification, Certificate, Document, ResearcherProfile
)

# ----------------------------------
# Document Admin
# ----------------------------------
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)

# ----------------------------------
# User Admin
# ----------------------------------
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

# ----------------------------------
# ResearcherProfile Admin
# ----------------------------------
@admin.register(ResearcherProfile)
class ResearcherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'institution', 'department', 'position')
    search_fields = ('user__username', 'email', 'name', 'institution', 'department', 'position')
    list_filter = ('department', 'institution')

# ----------------------------------
# Payment Admin Form & Admin
# ----------------------------------
class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lazy-load queryset to avoid InvalidCursorName
        self.fields['application'].queryset = Application.objects.all()


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm
    raw_id_fields = ('application',)
    list_display = ('control_number', 'researcher', 'amount', 'status', 'generated_date')
    list_filter = ('status', 'research_type', 'year')
    search_fields = ('control_number', 'researcher__username', 'researcher__email')









# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     form = PaymentAdminForm
#     raw_id_fields = ('application',)
#     list_display = (
#         'control_number',
#         'researcher',
#         'get_amount_with_currency',
#         'status',
#         'research_type',
#         'level',
#         'nationality',
#         'generated_date'
#     )
#     list_filter = ('status', 'research_type', 'year', 'level', 'nationality')
#     search_fields = ('control_number', 'researcher__username', 'researcher__email')

#     def get_amount_with_currency(self, obj):
#         return f"{obj.amount:,} {obj.currency}" if obj.amount and obj.currency else "-"
#     get_amount_with_currency.short_description = 'Amount'


# ----------------------------------
# Application Admin
# ----------------------------------
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'researcher', 'status', 'officer_feedback', 'submitted_at')
    search_fields = ('title', 'researcher__username', 'status', 'officer_feedback')
    list_filter = ('status', 'category')

# ----------------------------------
# Attachment Admin
# ----------------------------------
@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'file_type', 'file_path', 'uploaded_at')
    search_fields = ('application__title', 'file_type', 'original_filename')
    list_filter = ('file_type',)

# ----------------------------------
# Notification Admin
# ----------------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'status', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('status',)

# ----------------------------------
# Certificate Admin
# ----------------------------------
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'certificate_number', 'issued_date')
    search_fields = ('certificate_number', 'application__title')
    list_filter = ('issued_date',)
