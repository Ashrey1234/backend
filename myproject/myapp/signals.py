





# signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.db import transaction
# from .models import Application, Certificate
# from django.conf import settings
# import os
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.utils import ImageReader
# from textwrap import wrap


# def create_certificate_pdf(application_instance):
#     """
#     Generate PDF certificate for a given approved application.
#     Ensures officer feedback is included and saved in Certificate model.
#     """
#     # 🔹 Refresh to get latest data from DB
#     instance = Application.objects.get(id=application_instance.id)
    
#     researcher_name = instance.researcher.get_full_name() or instance.researcher.username

#     # 🔹 File paths
#     file_name = f"certificates/{instance.researcher.username}_{instance.id}.pdf"
#     os.makedirs(os.path.join(settings.MEDIA_ROOT, 'certificates'), exist_ok=True)
#     file_path = os.path.join(settings.MEDIA_ROOT, file_name)

#     # 🔹 PDF Generation
#     c = canvas.Canvas(file_path, pagesize=A4)
#     width, height = A4
#     margin = 50
#     spacing = 28

#     # Light blue background
#     c.setFillColorRGB(0.85, 0.95, 1)
#     c.rect(0, 0, width, height, fill=1)

#     # Border with shadow
#     shadow_offset = 5
#     c.setFillColor(colors.HexColor("#cccccc"))
#     c.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin,
#                 radius=20, fill=0, stroke=1)
#     c.setStrokeColor(colors.HexColor("#003366"))
#     c.setLineWidth(4)
#     c.roundRect(margin/2, margin/2, width - margin, height - margin,
#                 radius=20, fill=0, stroke=1)

#     # Watermark
#     c.saveState()
#     c.translate(width/2, height/2)
#     c.rotate(45)
#     c.setFont("Helvetica-Bold", 60)
#     try:
#         c.setFillAlpha(0.2)
#     except AttributeError:
#         pass
#     c.setFillColorRGB(0.3, 0.3, 0.3)
#     c.drawCentredString(0, 0, "ONLINE COPY")
#     c.restoreState()

#     # Logo
#     logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
#     logo_height = 120
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         logo_width = 120
#         c.drawImage(logo, (width - logo_width)/2, height - logo_height - margin,
#                     width=logo_width, height=logo_height, mask='auto')

#     # Certificate content
#     c.setFillColor(colors.black)
#     c.setFont("Helvetica-Bold", 26)
#     y = height - logo_height - margin - 40
#     c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

#     c.setFont("Helvetica", 16)
#     y -= spacing * 2

#     # Certificate number
#     c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#     y -= spacing

#     # Researcher name
#     c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#     y -= spacing

#     # Research title
#     max_chars_per_line = 60
#     title_lines = wrap(instance.title, max_chars_per_line)
#     for line in title_lines:
#         c.drawCentredString(width/2, y, f"Research Title: {line}" if line == title_lines[0] else line)
#         y -= spacing

#     # Officer feedback
#     feedback_text = instance.officer_feedback.strip() if instance.officer_feedback else "(No feedback given)"
#     feedback_lines = wrap(feedback_text, max_chars_per_line)
#     for i, line in enumerate(feedback_lines):
#         if i == 0:
#             c.drawCentredString(width/2, y, f"Officer Feedback: {line}")
#         else:
#             c.drawCentredString(width/2, y, line)
#         y -= spacing

#     # Issued date
#     c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")

#     # Signature
#     signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures', 'officer_signature.png')
#     if os.path.exists(signature_path):
#         signature_img = ImageReader(signature_path)
#         sig_width, sig_height = 150, 50
#         x_sig = width - sig_width - margin
#         y_sig = margin + 20
#         c.drawImage(signature_img, x_sig, y_sig, width=sig_width, height=sig_height, mask='auto')
#         c.setFont("Helvetica-Oblique", 14)
#         c.drawString(x_sig, y_sig - 20, "Research Officer")

#     c.showPage()
#     c.save()

#     # 🔹 Save or update Certificate model
#     Certificate.objects.update_or_create(
#         application=instance,
#         defaults={
#             "certificate_number": f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}",
#             "file_path": file_name,
#             "issued_date": timezone.now(),
#             "officer_feedback": instance.officer_feedback,  # Save feedback
#         }
#     )

#     # 🔹 Send email with certificate attached
#     subject = "Your Research Certificate has been issued"
#     message = f"""
# Hello {researcher_name},

# Congratulations! Your research application titled "{instance.title}" has been approved. 
# Please find your certificate attached.

# Best regards,
# Research Office
# """
#     email = EmailMessage(
#         subject=subject,
#         body=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[instance.researcher.email],
#     )
#     email.attach_file(file_path)
#     email.send(fail_silently=False)


# # ----------------------------
# # Signal
# # ----------------------------
# @receiver(post_save, sender=Application)
# def generate_or_update_certificate(sender, instance, **kwargs):
#     """
#     Trigger PDF creation only if status is Approved
#     and ensures latest feedback is included.
#     """
#     if instance.status == 'Approved':
#         transaction.on_commit(lambda: create_certificate_pdf(instance))























































































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.db import transaction
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.utils import timezone
# from .models import Application, Certificate
# import os
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.utils import ImageReader
# from textwrap import wrap

# def create_certificate_pdf(application_instance):
#     instance = Application.objects.get(id=application_instance.id)
#     researcher_name = instance.researcher.get_full_name() or instance.researcher.username

#     # -------------------------
#     # Paths
#     # -------------------------
#     online_file_name = f"{instance.researcher.username}_{instance.id}.pdf"
#     online_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', online_file_name)
#     os.makedirs(os.path.dirname(online_file_path), exist_ok=True)

#     offline_file_name = f"{instance.researcher.username}_{instance.id}_offline.pdf"
#     offline_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates/offline', offline_file_name)
#     os.makedirs(os.path.dirname(offline_file_path), exist_ok=True)

#     # -------------------------
#     # Online PDF (with watermark)
#     # -------------------------
#     c = canvas.Canvas(online_file_path, pagesize=A4)
#     width, height = A4
#     margin = 50
#     spacing = 28

#     # Background
#     c.setFillColorRGB(0.85, 0.95, 1)
#     c.rect(0, 0, width, height, fill=1)

#     # Border
#     shadow_offset = 5
#     c.setFillColor(colors.HexColor("#cccccc"))
#     c.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin, radius=20, fill=0, stroke=1)
#     c.setStrokeColor(colors.HexColor("#003366"))
#     c.setLineWidth(4)
#     c.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#     # Watermark
#     c.saveState()
#     c.translate(width/2, height/2)
#     c.rotate(45)
#     c.setFont("Helvetica-Bold", 60)
#     try:
#         c.setFillAlpha(0.2)
#     except AttributeError:
#         pass
#     c.setFillColorRGB(0.3, 0.3, 0.3)
#     c.drawCentredString(0, 0, "ONLINE COPY")
#     c.restoreState()

#     # Logo
#     logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         c.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#     # Content
#     y = height - 120 - margin - 40
#     c.setFont("Helvetica-Bold", 26)
#     c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

#     y -= spacing * 2
#     c.setFont("Helvetica", 16)
#     c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#     y -= spacing
#     c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#     y -= spacing

#     # Title
#     for line in wrap(instance.title, 60):
#         c.drawCentredString(width/2, y, line)
#         y -= spacing

#     # Officer feedback
#     feedback = instance.officer_feedback or "(No feedback given)"
#     for line in wrap(feedback, 60):
#         c.drawCentredString(width/2, y, line)
#         y -= spacing


  

#     # Issued date
#     c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")

#     # Signature
#     signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/officer_signature.png')
#     if os.path.exists(signature_path):
#         sig = ImageReader(signature_path)
#         c.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
#         c.setFont("Helvetica-Oblique", 14)
#         c.drawString(width - 150 - margin, margin, "Research Officer")

#     c.showPage()
#     c.save()

#     # -------------------------
#     # Offline PDF (without watermark)
#     # -------------------------
#     c_off = canvas.Canvas(offline_file_path, pagesize=A4)
#     width, height = A4
#     y = height - 120 - margin - 40

#     # Background & border same as online
#     c_off.setFillColorRGB(0.85, 0.95, 1)
#     c_off.rect(0, 0, width, height, fill=1)
#     c_off.setFillColor(colors.HexColor("#cccccc"))
#     c_off.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin, radius=20, fill=0, stroke=1)
#     c_off.setStrokeColor(colors.HexColor("#003366"))
#     c_off.setLineWidth(4)
#     c_off.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#     # Logo
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         c_off.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#     # Content
#     c_off.setFont("Helvetica-Bold", 26)
#     c_off.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")
#     y -= spacing * 2
#     c_off.setFont("Helvetica", 16)
#     c_off.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#     y -= spacing
#     c_off.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#     y -= spacing
#     for line in wrap(instance.title, 60):
#         c_off.drawCentredString(width/2, y, line)
#         y -= spacing
#     for line in wrap(feedback, 60):
#         c_off.drawCentredString(width/2, y, line)
#         y -= spacing
#     c_off.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
#     if os.path.exists(signature_path):
#         sig = ImageReader(signature_path)
#         c_off.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
#         c_off.setFont("Helvetica-Oblique", 14)
#         c_off.drawString(width - 150 - margin, margin, "Research Officer")
#     c_off.showPage()
#     c_off.save()

#     # -------------------------
#     # Save Certificate model
#     # -------------------------
#     Certificate.objects.update_or_create(
#         application=instance,
#         defaults={
#             "certificate_number": f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}",
#             "file_path": f"certificates/{online_file_name}",
#             "offline_file": f"certificates/offline/{offline_file_name}",
#             "issued_date": timezone.now(),
#             "officer_feedback": instance.officer_feedback,
#         }
#     )

#     # -------------------------
#     # Send email to researcher
#     # -------------------------
#     email = EmailMessage(
#         subject="Your Research Certificate has been issued",
#         body=f"Hello {researcher_name},\n\nYour research titled '{instance.title}' has been approved. Certificate attached.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[instance.researcher.email],
#     )
#     email.attach_file(online_file_path)
#     email.send(fail_silently=False)


# @receiver(post_save, sender=Application)
# def generate_or_update_certificate(sender, instance, **kwargs):
#     if instance.status == 'Approved':
#         transaction.on_commit(lambda: create_certificate_pdf(instance))





















# from django.db.models.signals import post_save                   fantastic amazing
# from django.dispatch import receiver
# from django.db import transaction
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.utils import timezone
# from .models import Application, Certificate
# import os
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.utils import ImageReader
# from textwrap import wrap

# def create_certificate_pdf(application_instance):
#     instance = Application.objects.get(id=application_instance.id)
#     researcher_name = instance.researcher.get_full_name() or instance.researcher.username

#     # -------------------------
#     # Paths
#     # -------------------------
#     online_file_name = f"{instance.researcher.username}_{instance.id}.pdf"
#     online_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', online_file_name)
#     os.makedirs(os.path.dirname(online_file_path), exist_ok=True)

#     offline_file_name = f"{instance.researcher.username}_{instance.id}_offline.pdf"
#     offline_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates/offline', offline_file_name)
#     os.makedirs(os.path.dirname(offline_file_path), exist_ok=True)

#     width, height = A4
#     margin = 50
#     spacing = 28
#     shadow_offset = 5

#     # -------------------------
#     # Online PDF (with watermark)
#     # -------------------------
#     c = canvas.Canvas(online_file_path, pagesize=A4)

#     # Background
#     c.setFillColorRGB(1, 1, 1)  # White background
#     c.rect(0, 0, width, height, fill=1)

#     # Border
#     c.setStrokeColor(colors.black)
#     c.setLineWidth(2)
#     c.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#     # Watermark
#     c.saveState()
#     c.translate(width/2, height/2)
#     c.rotate(45)
#     c.setFont("Helvetica-Bold", 60)
#     try:
#         c.setFillAlpha(0.1)  # light grey watermark
#     except AttributeError:
#         pass
#     c.setFillColor(colors.grey)
#     c.drawCentredString(0, 0, "ONLINE COPY")
#     c.restoreState()

#     # Logo
#     logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         c.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#     # Content
#     y = height - 120 - margin - 40
#     c.setFont("Helvetica-Bold", 26)
#     c.setFillColor(colors.black)
#     c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

#     y -= spacing * 2
#     c.setFont("Helvetica", 16)
#     c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#     y -= spacing
#     c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#     y -= spacing

#     # Research Title
#     for i, line in enumerate(wrap(instance.title, 60)):
#         if i == 0:
#             c.drawCentredString(width/2, y, f"Research Title: {line}")
#         else:
#             c.drawCentredString(width/2, y, line)
#         y -= spacing

#     # Officer Feedback
#     feedback = instance.officer_feedback or "(No feedback given)"
#     for i, line in enumerate(wrap(feedback, 60)):
#         if i == 0:
#             c.drawCentredString(width/2, y, f"Officer Feedback: {line}")
#         else:
#             c.drawCentredString(width/2, y, line)
#         y -= spacing

#     # Issued date
#     c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")

#     # Signature
#     signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/officer_signature.png')
#     if os.path.exists(signature_path):
#         sig = ImageReader(signature_path)
#         c.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
#         c.setFont("Helvetica-Oblique", 14)
#         c.drawString(width - 150 - margin, margin, "Research Officer")

#     c.showPage()
#     c.save()

#     # -------------------------
#     # Offline PDF (without watermark)
#     # -------------------------
#     c_off = canvas.Canvas(offline_file_path, pagesize=A4)

#     # Background & border same as online
#     c_off.setFillColorRGB(1, 1, 1)  # White
#     c_off.rect(0, 0, width, height, fill=1)
#     c_off.setStrokeColor(colors.black)
#     c_off.setLineWidth(2)
#     c_off.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#     # Logo
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         c_off.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#     y = height - 120 - margin - 40
#     c_off.setFont("Helvetica-Bold", 26)
#     c_off.setFillColor(colors.black)
#     c_off.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")
#     y -= spacing * 2
#     c_off.setFont("Helvetica", 16)
#     c_off.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#     y -= spacing
#     c_off.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#     y -= spacing
#     for i, line in enumerate(wrap(instance.title, 60)):
#         if i == 0:
#             c_off.drawCentredString(width/2, y, f"Research Title: {line}")
#         else:
#             c_off.drawCentredString(width/2, y, line)
#         y -= spacing
#     for i, line in enumerate(wrap(feedback, 60)):
#         if i == 0:
#             c_off.drawCentredString(width/2, y, f"Officer Feedback: {line}")
#         else:
#             c_off.drawCentredString(width/2, y, line)
#         y -= spacing
#     c_off.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
#     if os.path.exists(signature_path):
#         sig = ImageReader(signature_path)
#         c_off.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
#         c_off.setFont("Helvetica-Oblique", 14)
#         c_off.drawString(width - 150 - margin, margin, "Research Officer")
#     c_off.showPage()
#     c_off.save()

#     # -------------------------
#     # Save Certificate model
#     # -------------------------
#     Certificate.objects.update_or_create(
#         application=instance,
#         defaults={
#             "certificate_number": f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}",
#             "file_path": f"certificates/{online_file_name}",
#             "offline_file": f"certificates/offline/{offline_file_name}",
#             "issued_date": timezone.now(),
#             "officer_feedback": instance.officer_feedback,
#         }
#     )

#     # -------------------------
#     # Send email
#     # -------------------------
#     email = EmailMessage(
#         subject="Your Research Certificate has been issued",
#         body=f"Hello {researcher_name},\n\nYour research titled '{instance.title}' has been approved. Certificate attached.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[instance.researcher.email],
#     )
#     email.attach_file(online_file_path)
#     email.send(fail_silently=False)


# @receiver(post_save, sender=Application)
# def generate_or_update_certificate(sender, instance, **kwargs):
#     if instance.status == 'Approved':
#         transaction.on_commit(lambda: create_certificate_pdf(instance))








from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from textwrap import wrap
from .models import Application, Certificate
from django.db import transaction
import os
import qrcode

def create_certificate_pdf(application_instance):
    instance = Application.objects.get(id=application_instance.id)
    researcher_name = instance.researcher.get_full_name() or instance.researcher.username

    # Paths
    online_file_name = f"{instance.researcher.username}_{instance.id}.pdf"
    online_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', online_file_name)
    os.makedirs(os.path.dirname(online_file_path), exist_ok=True)

    offline_file_name = f"{instance.researcher.username}_{instance.id}_offline.pdf"
    offline_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates/offline', offline_file_name)
    os.makedirs(os.path.dirname(offline_file_path), exist_ok=True)

    width, height = A4
    margin = 50
    spacing = 28

    # -------------------------
    # Helper function to draw content
    # -------------------------
    def draw_certificate(c, watermark=False):
        # Background
        c.setFillColorRGB(1, 1, 1)  # white background
        c.rect(0, 0, width, height, fill=1)

        # Border
        shadow_offset = 5
        c.setFillColor(colors.HexColor("#cccccc"))
        c.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin, radius=20, fill=0, stroke=1)
        c.setStrokeColor(colors.HexColor("#003366"))
        c.setLineWidth(4)
        c.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

        # Watermark
        if watermark:
            c.saveState()
            c.translate(width/2, height/2)
            c.rotate(45)
            c.setFont("Helvetica-Bold", 60)
            try:
                c.setFillAlpha(0.1)
            except AttributeError:
                pass
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawCentredString(0, 0, "ONLINE COPY")
            c.restoreState()

        # Logo
        logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
        if os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            c.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

        # Heading
        y = height - 120 - margin - 40
        c.setFont("Times-Bold", 28)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

        y -= spacing * 2
        c.setFont("Helvetica", 16)

        # Certificate Number
        c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
        y -= spacing

        # Researcher
        c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
        y -= spacing

        # Title
        title_lines = wrap(instance.title, 60)
        for i, line in enumerate(title_lines):
            c.drawCentredString(width/2, y, f"Research Title: {line}" if i == 0 else line)
            y -= spacing

        # Officer feedback
        feedback_text = instance.officer_feedback or "(No feedback given)"
        feedback_lines = wrap(feedback_text, 60)
        for i, line in enumerate(feedback_lines):
            c.drawCentredString(width/2, y, f"Officer Feedback: {line}" if i == 0 else line)
            y -= spacing

        # Issued date
        c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
        y -= spacing

        # Signature
        signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/officer_signature.png')
        if os.path.exists(signature_path):
            sig = ImageReader(signature_path)
            c.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
            c.setFont("Helvetica-Oblique", 14)
            c.drawString(width - 150 - margin, margin, "Research Officer")

        # QR Code
        # qr_url = f"https://example.com/verify_certificate/{instance.id}/"
        qr_url = f"http://127.0.0.1:8000/verify_certificate/{instance.id}/"
        qr = qrcode.make(qr_url)
        qr_path = os.path.join(settings.MEDIA_ROOT, f'certificates/qr_{instance.id}.png')
        qr.save(qr_path)
        qr_img = ImageReader(qr_path)
        c.drawImage(qr_img, margin + 10, margin + 10, width=80, height=80)

        c.showPage()

    # Generate PDFs
    c_online = canvas.Canvas(online_file_path, pagesize=A4)
    draw_certificate(c_online, watermark=True)
    c_online.save()

    c_offline = canvas.Canvas(offline_file_path, pagesize=A4)
    draw_certificate(c_offline, watermark=False)
    c_offline.save()

    # Save Certificate model
    Certificate.objects.update_or_create(
        application=instance,
        defaults={
            "certificate_number": f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}",
            "file_path": f"certificates/{online_file_name}",
            "offline_file": f"certificates/offline/{offline_file_name}",
            "issued_date": timezone.now(),
            "officer_feedback": instance.officer_feedback,
        }
    )

    # Send email
    email = EmailMessage(
        subject="Your Research Certificate has been issued",
        body=f"Hello {researcher_name},\n\nYour research titled '{instance.title}' has been approved. Certificate attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.researcher.email],
    )
    email.attach_file(online_file_path)
    email.send(fail_silently=False)


# Signal
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Application)
def generate_or_update_certificate(sender, instance, **kwargs):
    if instance.status == 'Approved':
        transaction.on_commit(lambda: create_certificate_pdf(instance))
