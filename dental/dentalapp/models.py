from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model inheriting from AbstractUser
class User(AbstractUser):
    identitycardno = models.CharField(max_length=12, unique=True)
    fullname = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()

    # Role field: 0 for admin, 1 for doctor, 2 for client
    ADMIN = 0
    DOCTOR = 1
    CLIENT = 2
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (DOCTOR, 'Doctor'),
        (CLIENT, 'Client'),
    ]
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CLIENT)

    # Avoid conflicts with Django's default group and permission fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

# Doctor model extending from User
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.DOCTOR})
    specialization = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)    

    def __str__(self):
        return self.user.fullname

# Admin model extending from User
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': User.ADMIN})
    position = models.CharField(max_length=255)

    def __str__(self):
        return self.user.fullname

# Service model
class Service(models.Model):
    CONSULTATION = 'Consultation'
    SURGERY = 'Surgery'
    CLEANING = 'Cleaning'
    CHECKUP = 'Checkup'
    
    SERVICE_TYPE_CHOICES = [
        (CONSULTATION, 'Consultation'),
        (SURGERY, 'Surgery'),
        (CLEANING, 'Cleaning'),
        (CHECKUP, 'Checkup'),
    ]

    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    service_detail = models.TextField()

    def __str__(self):
        return self.service_name


# Appointment model
class Appointment(models.Model):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]

    
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    appointment_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    client = models.CharField(max_length=50, null=True)



    def __str__(self):
        return f"Appointment with Dr. {self.doctor.fullname} for {self.service.service_name} on {self.date} at {self.time}"


