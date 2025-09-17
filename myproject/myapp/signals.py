
# from reportlab.lib.pagesizes import A4               
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.lib.utils import ImageReader
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.utils import timezone
# from textwrap import wrap
# from .models import Application, Certificate
# from django.db import transaction
# import os
# import qrcode

# def create_certificate_pdf(application_instance):
#     instance = Application.objects.get(id=application_instance.id)
#     researcher_name = instance.researcher.get_full_name() or instance.researcher.username

#     # Paths
#     online_file_name = f"{instance.researcher.username}_{instance.id}.pdf"
#     online_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', online_file_name)
#     os.makedirs(os.path.dirname(online_file_path), exist_ok=True)

#     offline_file_name = f"{instance.researcher.username}_{instance.id}_offline.pdf"
#     offline_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates/offline', offline_file_name)
#     os.makedirs(os.path.dirname(offline_file_path), exist_ok=True)

#     width, height = A4
#     margin = 50
#     spacing = 28

#     # -------------------------
#     # Helper function to draw content
#     # -------------------------
#     def draw_certificate(c, watermark=False):
#         # Background
#         c.setFillColorRGB(1, 1, 1)  # white background
#         c.rect(0, 0, width, height, fill=1)

#         # Border
#         shadow_offset = 5
#         c.setFillColor(colors.HexColor("#cccccc"))
#         c.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin, radius=20, fill=0, stroke=1)
#         c.setStrokeColor(colors.HexColor("#003366"))
#         c.setLineWidth(4)
#         c.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#         # Watermark
#         if watermark:
#             c.saveState()
#             c.translate(width/2, height/2)
#             c.rotate(45)
#             c.setFont("Helvetica-Bold", 60)
#             try:
#                 c.setFillAlpha(0.1)
#             except AttributeError:
#                 pass
#             c.setFillColorRGB(0.3, 0.3, 0.3)
#             c.drawCentredString(0, 0, "ONLINE COPY")
#             c.restoreState()

#         # Logo
#         logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
#         if os.path.exists(logo_path):
#             logo = ImageReader(logo_path)
#             c.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#         # Heading
#         y = height - 120 - margin - 40
#         c.setFont("Times-Bold", 28)
#         c.setFillColor(colors.black)
#         c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

#         y -= spacing * 2
#         c.setFont("Helvetica", 16)

#         # Certificate Number
#         c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#         y -= spacing

#         # Researcher
#         c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#         y -= spacing

#         # Title
#         title_lines = wrap(instance.title, 60)
#         for i, line in enumerate(title_lines):
#             c.drawCentredString(width/2, y, f"Research Title: {line}" if i == 0 else line)
#             y -= spacing

#         # Officer feedback
#         feedback_text = instance.officer_feedback or "(No feedback given)"
#         feedback_lines = wrap(feedback_text, 60)
#         for i, line in enumerate(feedback_lines):
#             c.drawCentredString(width/2, y, f"Officer Feedback: {line}" if i == 0 else line)
#             y -= spacing

#         # Issued date
#         c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
#         y -= spacing

#         # # Signature
#         # signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/officer_signature.png')
#         # if os.path.exists(signature_path):
#         #     sig = ImageReader(signature_path)
#         #     c.drawImage(sig, width - 150 - margin, margin + 20, width=150, height=50, mask='auto')
#         #     c.setFont("Helvetica-Oblique", 14)
#         #     c.drawString(width - 150 - margin, margin, "Research Officer")


    

#         # QR Code
#         # qr_url = f"https://example.com/verify_certificate/{instance.id}/"
#         # qr_url = f"http://127.0.0.1:8000/verify_certificate/{instance.id}/"
#         qr_url = f"http://10.176.247.177:8000/verify_certificate/{instance.id}/"
#         qr = qrcode.make(qr_url)
#         qr_path = os.path.join(settings.MEDIA_ROOT, f'certificates/qr_{instance.id}.png')
#         qr.save(qr_path)
#         qr_img = ImageReader(qr_path)
#         c.drawImage(qr_img, margin + 10, margin + 10, width=80, height=80)

#         c.showPage()

#     # Generate PDFs
#     c_online = canvas.Canvas(online_file_path, pagesize=A4)
#     draw_certificate(c_online, watermark=True)
#     c_online.save()

#     c_offline = canvas.Canvas(offline_file_path, pagesize=A4)
#     draw_certificate(c_offline, watermark=False)
#     c_offline.save()

#     # Save Certificate model
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

#     # Send email
#     email = EmailMessage(
#         subject="Your Research Certificate has been issued",
#         body=f"Hello {researcher_name},\n\nYour research titled '{instance.title}' has been approved. Certificate attached.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[instance.researcher.email],
#     )
#     email.attach_file(online_file_path)
#     email.send(fail_silently=False)


# # Signal
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=Application)
# def generate_or_update_certificate(sender, instance, **kwargs):
#     if instance.status == 'Approved':
#         transaction.on_commit(lambda: create_certificate_pdf(instance))









# from reportlab.lib.pagesizes import A4        signature
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.lib.utils import ImageReader
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.utils import timezone
# from textwrap import wrap
# from .models import Application, Certificate
# from django.db import transaction
# import os
# import qrcode

# def create_certificate_pdf(application_instance):
#     instance = Application.objects.get(id=application_instance.id)
#     researcher_name = instance.researcher.get_full_name() or instance.researcher.username

#     # Paths
#     online_file_name = f"{instance.researcher.username}_{instance.id}.pdf"
#     online_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', online_file_name)
#     os.makedirs(os.path.dirname(online_file_path), exist_ok=True)

#     offline_file_name = f"{instance.researcher.username}_{instance.id}_offline.pdf"
#     offline_file_path = os.path.join(settings.MEDIA_ROOT, 'certificates/offline', offline_file_name)
#     os.makedirs(os.path.dirname(offline_file_path), exist_ok=True)

#     width, height = A4
#     margin = 50
#     spacing = 28

#     # -------------------------
#     # Helper function to draw content
#     # -------------------------
#     def draw_certificate(c, watermark=False):
#         # Background
#         c.setFillColorRGB(1, 1, 1)
#         c.rect(0, 0, width, height, fill=1)

#         # Border
#         shadow_offset = 5
#         c.setFillColor(colors.HexColor("#cccccc"))
#         c.roundRect(margin/2 + shadow_offset, margin/2 - shadow_offset, width - margin, height - margin, radius=20, fill=0, stroke=1)
#         c.setStrokeColor(colors.HexColor("#003366"))
#         c.setLineWidth(4)
#         c.roundRect(margin/2, margin/2, width - margin, height - margin, radius=20, fill=0, stroke=1)

#         # Watermark
#         if watermark:
#             c.saveState()
#             c.translate(width/2, height/2)
#             c.rotate(45)
#             c.setFont("Helvetica-Bold", 60)
#             try:
#                 c.setFillAlpha(0.1)
#             except AttributeError:
#                 pass
#             c.setFillColorRGB(0.3, 0.3, 0.3)
#             c.drawCentredString(0, 0, "ONLINE COPY")
#             c.restoreState()

#         # Logo
#         logo_path = os.path.join(settings.BASE_DIR, 'media/logo/zafiri_logo.png')
#         if os.path.exists(logo_path):
#             logo = ImageReader(logo_path)
#             c.drawImage(logo, (width - 120)/2, height - 120 - margin, width=120, height=120, mask='auto')

#         # Heading
#         y = height - 120 - margin - 40
#         c.setFont("Times-Bold", 28)
#         c.setFillColor(colors.black)
#         c.drawCentredString(width/2, y, "RESEARCH CERTIFICATE")

#         y -= spacing * 2
#         c.setFont("Helvetica", 16)

#         # Certificate Number
#         c.drawCentredString(width/2, y, f"Certificate Number: CERT-{instance.id}-{timezone.now().strftime('%Y%m%d')}")
#         y -= spacing

#         # Researcher
#         c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
#         y -= spacing

#         # Title
#         title_lines = wrap(instance.title, 60)
#         for i, line in enumerate(title_lines):
#             c.drawCentredString(width/2, y, f"Research Title: {line}" if i == 0 else line)
#             y -= spacing

#         # Officer feedback
#         feedback_text = instance.officer_feedback or "(No feedback given)"
#         feedback_lines = wrap(feedback_text, 60)
#         for i, line in enumerate(feedback_lines):
#             c.drawCentredString(width/2, y, f"Officer Feedback: {line}" if i == 0 else line)
#             y -= spacing

#         # Issued date
#         c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
#         y -= spacing

#         # Signature
#         signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/signature12.png')
#         if os.path.exists(signature_path):
#             sig = ImageReader(signature_path)
#             sig_width = 150
#             sig_height = 50
#             sig_x = width - sig_width - margin
#             sig_y = margin + 50
#             c.drawImage(sig, sig_x, sig_y, width=sig_width, height=sig_height, mask='auto')

#             # Jina na cheo chini ya signature
#             officer_name = "Dr. Aisha Salim Ali"  # Badilisha kutoka DB ikiwa unataka
#             officer_title = "Research Officer"  # Badilisha kutoka DB ikiwa unataka
#             c.setFont("Helvetica-Bold", 12)
#             c.drawCentredString(sig_x + sig_width / 2, sig_y - 15, officer_name)
#             c.setFont("Helvetica-Oblique", 10)
#             c.drawCentredString(sig_x + sig_width / 2, sig_y - 30, officer_title)

#         # QR Code
#         qr_url = f"http://10.176.247.177:8000/verify_certificate/{instance.id}/"
#         qr = qrcode.make(qr_url)
#         qr_path = os.path.join(settings.MEDIA_ROOT, f'certificates/qr_{instance.id}.png')
#         qr.save(qr_path)
#         qr_img = ImageReader(qr_path)
#         c.drawImage(qr_img, margin + 10, margin + 10, width=80, height=80)

#         c.showPage()

#     # Generate PDFs
#     c_online = canvas.Canvas(online_file_path, pagesize=A4)
#     draw_certificate(c_online, watermark=True)
#     c_online.save()

#     c_offline = canvas.Canvas(offline_file_path, pagesize=A4)
#     draw_certificate(c_offline, watermark=False)
#     c_offline.save()

#     # Save Certificate model
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

#     # Send email
#     email = EmailMessage(
#         subject="Your Research Certificate has been issued",
#         body=f"Hello {researcher_name},\n\nYour research titled '{instance.title}' has been approved. Certificate attached.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[instance.researcher.email],
#     )
#     email.attach_file(online_file_path)
#     email.send(fail_silently=False)


# # Signal
# from django.db.models.signals import post_save
# from django.dispatch import receiver

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
    """
    Generate both online and offline certificates for an approved application.
    """
    # Fetch the latest Application instance to get updated feedback
    instance = Application.objects.get(id=application_instance.id)
    researcher_name = instance.researcher.get_full_name() or instance.researcher.username

    # Get or create Certificate instance
    certificate_instance, _ = Certificate.objects.get_or_create(
        application=instance,
        defaults={
            'certificate_number': f"CERT-{instance.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            'officer_feedback': instance.officer_feedback
        }
    )

    # Ensure officer_feedback is up-to-date
    if not certificate_instance.officer_feedback and instance.officer_feedback:
        certificate_instance.officer_feedback = instance.officer_feedback
        certificate_instance.save()

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

    def draw_certificate(c, watermark=False):
        # Background
        c.setFillColorRGB(1, 1, 1)
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
        c.drawCentredString(width/2, y, f"Certificate Number: {certificate_instance.certificate_number}")
        y -= spacing

        # Researcher
        c.drawCentredString(width/2, y, f"Researcher: {researcher_name}")
        y -= spacing

        # Title
        title_lines = wrap(instance.title, 60)
        for i, line in enumerate(title_lines):
            c.drawCentredString(width/2, y, f"Research Title: {line}" if i == 0 else line)
            y -= spacing

        # Officer feedback (from Certificate instance)
        feedback_text = certificate_instance.officer_feedback or "(No feedback given)"
        feedback_lines = wrap(feedback_text, 60)
        for i, line in enumerate(feedback_lines):
            c.drawCentredString(width/2, y, f"Officer Feedback: {line}" if i == 0 else line)
            y -= spacing

        # Issued date
        c.drawCentredString(width/2, y, f"Issued On: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
        y -= spacing

        # Signature
        signature_path = os.path.join(settings.MEDIA_ROOT, 'signatures/signature12.png')
        if os.path.exists(signature_path):
            sig = ImageReader(signature_path)
            sig_width = 150
            sig_height = 50
            sig_x = width - sig_width - margin
            sig_y = margin + 50
            c.drawImage(sig, sig_x, sig_y, width=sig_width, height=sig_height, mask='auto')

            # Officer name & title
            officer_name = "Dr. Aisha Salim Ali"
            officer_title = "Research Officer"
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(sig_x + sig_width / 2, sig_y - 15, officer_name)
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(sig_x + sig_width / 2, sig_y - 30, officer_title)

        # QR Code
        qr_url = f"http://10.176.247.177:8000/verify_certificate/{instance.id}/"
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

    # Update Certificate model with file paths
    certificate_instance.file_path.name = f"certificates/{online_file_name}"
    certificate_instance.offline_file.name = f"certificates/offline/{offline_file_name}"
    certificate_instance.issued_date = timezone.now()
    certificate_instance.save()

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
        # Ensure PDF is generated AFTER transaction commits (feedback saved)
        transaction.on_commit(lambda: create_certificate_pdf(instance))
        
        
        
        
        
        
        
        