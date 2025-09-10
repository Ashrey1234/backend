# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from .models import Application, Certificate
# import os
# from django.conf import settings

# @receiver(post_save, sender=Application)
# def generate_certificate(sender, instance, created, **kwargs):
#     """
#     Generates a certificate automatically when an Application is approved.
#     """
#     # Check if application is approved and no certificate exists yet
#     if instance.status == 'Approved' and not Certificate.objects.filter(application=instance).exists():

#         # Get researcher name
#         researcher_name = getattr(getattr(instance.researcher, 'profile', None), 'name', None) \
#                           or instance.researcher.get_full_name() \
#                           or instance.researcher.username

#         # Generate certificate number
#         certificate_number = f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}"

#         # Prepare file path
#         file_name = f"certificates/{instance.researcher.username}_{instance.id}.txt"
#         full_path = os.path.join(settings.MEDIA_ROOT, file_name)
#         os.makedirs(os.path.dirname(full_path), exist_ok=True)

#         # Certificate content
#         content = f"""
# Certificate Number: {certificate_number}
# Researcher: {researcher_name}
# Research Title: {instance.title}
# Officer Feedback: {instance.officer_feedback or 'No feedback provided'}
# Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}
# """

#         # Write to file
#         try:
#             with open(full_path, 'w') as f:
#                 f.write(content)
#         except Exception as e:
#             print(f"Error writing certificate file: {e}")

#         # Create Certificate object in DB
#         Certificate.objects.create(
#             application=instance,
#             certificate_number=certificate_number,
#             file_path=file_name,
#             issued_date=timezone.now()
#         )




























# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import EmailMessage
from .models import Application, Certificate
import os
from django.conf import settings

@receiver(post_save, sender=Application)
def generate_certificate(sender, instance, created, **kwargs):
    # Tazama kama application imeapproved na certificate bado haijazalishwa
    if instance.status == 'Approved' and not Certificate.objects.filter(application=instance).exists():
        # Get researcher name
        if hasattr(instance.researcher, 'profile'):
            researcher_name = instance.researcher.profile.name
        else:
            researcher_name = instance.researcher.get_full_name() or instance.researcher.username

        # Generate certificate number na file path
        certificate_number = f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}"
        file_name = f"certificates/{instance.researcher.username}_{instance.id}.txt"
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'certificates'), exist_ok=True)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Andika content ya certificate
        content = f"""
Certificate Number: {certificate_number}
Researcher: {researcher_name}
Research Title: {instance.title}
Officer Feedback: {instance.officer_feedback or 'No feedback provided'}
Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}
"""
        with open(file_path, 'w') as f:
            f.write(content)

        # Create Certificate object
        certificate = Certificate.objects.create(
            application=instance,
            certificate_number=certificate_number,
            file_path=file_name,
            issued_date=timezone.now()
        )

        # Tuma email kwa researcher
        subject = "Your Research Certificate has been issued"
        message = f"""
Hello {researcher_name},

Congratulations! Your research application titled "{instance.title}" has been approved. 
Please find your certificate attached.

You can also view your application here: {settings.FRONTEND_URL}/applications/{instance.id}

Best regards,
Research Office
"""
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.researcher.email],
        )
        email.attach_file(file_path)
        email.send(fail_silently=False)
