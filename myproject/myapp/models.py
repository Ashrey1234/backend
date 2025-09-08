import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# ----------------------------
# Custom User Model
# ----------------------------
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    TYPE_CHOICES = [
        ('Student', 'Student'),
        ('University', 'University'),
        ('Institute', 'Institute'),
        ('Independent', 'Independent'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True)

    research_type = models.CharField(
        max_length=100,
        choices=[
            ('Environment & Marine', 'Environment & Marine'),
            ('Aquatic Organisms', 'Aquatic Organisms'),
            ('Fisheries Research', 'Fisheries Research'),
        ],
        blank=True,
        null=True
    )

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Officer', 'Officer'),
        ('Researcher', 'Researcher'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Researcher')

    institution = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    profile_completion = models.IntegerField(default=0)
    first_login = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group', related_name='myapp_user_groups', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='myapp_user_permissions', blank=True
    )

    def __str__(self):
        return self.username


# ----------------------------
# Application Model
# ----------------------------
class Application(models.Model):
    researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[('Draft', 'Draft'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Draft'
    )
    officer_feedback = models.TextField(blank=True, null=True)
    # submitted = models.CharField(max_length=100, blank=True, null=True)
    # submitted = models.CharField(max_length=100, blank=True, null=True)

    important = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.researcher.username}"


# ----------------------------
# Payment Model
# ----------------------------
class Payment(models.Model):
    researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    application = models.OneToOneField(
        Application,
        on_delete=models.PROTECT,
        related_name='payment_record',
        null=True, blank=True
    )
    research_type = models.CharField(
        max_length=100,
        choices=[
            ('Environment & Marine', 'Environment & Marine'),
            ('Aquatic Organisms', 'Aquatic Organisms'),
            ('Fisheries Research', 'Fisheries Research')
        ],
        default='Environment & Marine'
    )
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(datetime.datetime.now().year + 5)]
    )
    control_number = models.CharField(max_length=12, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Verified', 'Verified'), ('Expired', 'Expired')]
    )
    expiry_date = models.DateTimeField()
    used_for_application = models.BooleanField(default=False)
    generated_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.control_number:
            self.control_number = self.generate_control_number()
        if not self.amount or self.amount == 0:
            self.amount = self.calculate_fee()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_control_number():
        last = Payment.objects.order_by('-id').first()
        if last and last.control_number and last.control_number.isdigit():
            next_num = int(last.control_number) + 1
        else:
            next_num = 200050000000
        return str(next_num).zfill(12)

    def calculate_fee(self):
        # simplified fee calculation
        return 100000  # adjust as needed

    def __str__(self):
        return f"Payment {self.control_number} - {self.researcher.username}"













# ----------------------------
# Attachment Model
# ----------------------------
class Attachment(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file_type = models.CharField(
        max_length=50,
        choices=[('Makamu Form', 'Makamu Form'), ('Proposal', 'Proposal'), ('Ethical Form', 'Ethical Form')]
    )
    file_path = models.FileField(upload_to='attachments/%Y/%m/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    original_filename = models.CharField(max_length=255, default="unknown")
    file_size = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('application', 'file_type')
        ordering = ['file_type']

    def save(self, *args, **kwargs):
        if self.file_path:
            self.original_filename = self.file_path.name
            self.file_size = self.file_path.size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_type} - {self.application.title}"


# ----------------------------
# Document Model
# ----------------------------
class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# ----------------------------
# Notification Model
# ----------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('Read', 'Read'), ('Unread', 'Unread')], default='Unread')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"


# ----------------------------
# Certificate Model
# ----------------------------
class Certificate(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=50)
    file_path = models.FileField(upload_to='certificates/')
    issued_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.application.title}"


# ----------------------------
# Researcher Profile Model
# ----------------------------
class ResearcherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')])
    research_interests = models.JSONField(default=list)
    bio = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
