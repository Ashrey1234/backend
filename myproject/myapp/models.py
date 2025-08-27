import random
from django.db import transaction
from django.db import models

# Model for storing documents to be displayed on the frontend
class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.contrib.auth.models import AbstractUser

# Custom User
class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Officer', 'Officer'),
        ('Researcher', 'Researcher'),
    ]
    type = models.CharField(max_length=50, choices=[('Student','Student'),('University','University'),('Institute','Institute'),('Independent','Independent')], blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    country = models.CharField(max_length=100, blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myapp_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myapp_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class ResearcherProfile(models.Model):
    researcher = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)
    system_id = models.CharField(max_length=50, unique=True)

class Payment(models.Model):
    researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    research_type = models.CharField(
        max_length=100,
        choices=[
            ('Environment & Marine', 'Environment & Marine'),
            ('Aquatic Organisms', 'Aquatic Organisms'),
            ('Fisheries Research', 'Fisheries Research')
        ],
        default='Environment & Marine'
    )
    control_number = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Verified','Verified'),('Expired','Expired')])
    generated_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.control_number:
            self.control_number = self.generate_control_number()
        if not self.amount or self.amount == 0:
            self.amount = self.calculate_fee()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_control_number():
        # Find the latest control number and increment, or start at 200050000000
        last = Payment.objects.order_by('-id').first()
        if last and last.control_number and last.control_number.isdigit():
            next_num = int(last.control_number) + 1
            if len(str(next_num)) < 12:
                next_num = int('200050000000') + last.id + 1
        else:
            next_num = 200050000000
        return str(next_num).zfill(12)

    def calculate_fee(self):
        # Defensive: handle missing researcher or fields
        researcher = getattr(self, 'researcher', None)
        nationality = ''
        category = 'student'
        program_level = 'undergraduate'
        if researcher:
            nationality = (getattr(researcher, 'country', '') or '').lower()
            category = (getattr(researcher, 'role', '') or 'student').lower()
            program_level = (getattr(researcher, 'type', '') or 'undergraduate').lower()
        research_type = getattr(self, 'research_type', '').lower() if hasattr(self, 'research_type') else ''

        is_foreign = nationality not in ['tanzania', 'tz', '']

        # Fee table (same for all research types, but you can expand if needed)
        fee_table = {
            'local': {
                'student': {'undergraduate': 100000, 'master': 150000, 'phd': 200000},
                'university': {'undergraduate': 200000, 'master': 250000, 'phd': 300000},
                'institute': {'undergraduate': 300000, 'master': 350000, 'phd': 400000},
                'independent': {'undergraduate': 400000, 'master': 450000, 'phd': 500000},
            },
            'foreign': {
                'student': {'undergraduate': 430, 'master': 645, 'phd': 860},
                'university': {'undergraduate': 860, 'master': 1075, 'phd': 1290},
                'institute': {'undergraduate': 1290, 'master': 1505, 'phd': 1720},
                'independent': {'undergraduate': 1720, 'master': 1935, 'phd': 2150},
            }
        }

        key_nat = 'foreign' if is_foreign else 'local'
        key_cat = category if category in fee_table[key_nat] else 'student'
        key_prog = program_level if program_level in fee_table[key_nat][key_cat] else 'undergraduate'
        fee = fee_table[key_nat][key_cat][key_prog]
        return fee

class Application(models.Model):
    researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected')], default='Pending')
    officer_feedback = models.TextField(blank=True, null=True)

class Attachment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=[('Makamu Form','Makamu Form'),('Proposal','Proposal'),('Ethical Form','Ethical Form')])
    file_path = models.FileField(upload_to='attachments/')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('Read','Read'),('Unread','Unread')], default='Unread')
    created_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    certificate_number = models.CharField(max_length=50)
    file_path = models.FileField(upload_to='certificates/')
    issued_date = models.DateTimeField(auto_now_add=True)
