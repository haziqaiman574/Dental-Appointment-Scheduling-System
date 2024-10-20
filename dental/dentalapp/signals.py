# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User, Doctor

# @receiver(post_save, sender=User)
# def create_doctor_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.DOCTOR:
#         Doctor.objects.create(user=instance, specialization="General", qualification="MBBS")
