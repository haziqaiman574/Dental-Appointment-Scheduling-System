from django.contrib import admin
from .models import User, Doctor, Admin as AdminModel, Service, Appointment

# Custom UserAdmin to display user details properly in the admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'identitycardno', 'role')
    search_fields = ('username', 'fullname', 'identitycardno')
    list_filter = ('role',)

# Register the User model
admin.site.register(User, UserAdmin)

# Register the Doctor model
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'qualification')
    search_fields = ('user__fullname', 'specialization')

admin.site.register(Doctor, DoctorAdmin)

# Register the Admin model
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__fullname', 'position')

admin.site.register(AdminModel, AdminModelAdmin)

# Register the Service model
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'service_name', 'service_type')
    search_fields = ('service_name',)
    list_filter = ('service_type',)

admin.site.register(Service, ServiceAdmin)

# Register the Appointment model
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'service', 'date', 'time', 'appointment_status')
    search_fields = ('doctor__fullname', 'service__service_name', 'appointment_status')
    list_filter = ('appointment_status', 'date')

admin.site.register(Appointment, AppointmentAdmin)
