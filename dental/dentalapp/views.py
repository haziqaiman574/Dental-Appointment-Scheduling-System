from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Service
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import messages
from .forms import UserForm, CustomLoginForm, ServiceForm, AppointmentForm
from django.contrib.auth import login, authenticate

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import redirect
from .models import Appointment
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment, Doctor, Service, User, Admin
from .forms import AppointmentForm

@login_required
# Create your views here.
def homepage(request):
    return render(request, 'dashboard/homepage.html')

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})
    

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance but don’t save yet
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'dashboard/user_form.html', {'form': form})

@login_required
def user_update(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance but don’t save yet
            new_password = form.cleaned_data['new_password']
            if new_password:  # Only set a new password if provided
                user.set_password(new_password)  # Hash the new password
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'dashboard/user_form.html', {'form': form})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')
    return render(request, 'dashboard/user_confirm_delete.html', {'user': user})

class LoginView(AuthLoginView):
    template_name = 'dashboard/login.html'  # Specify your login template

    def form_valid(self, form):
        # Call the original form_valid method to log the user in
        login(self.request, form.get_user())
        return redirect('homepage')  # Redirect to a home page or dashboard after successful login

class LogoutView(AuthLogoutView):
    next_page = 'login'  # Redirect to login page after logout

@login_required
def services(request):
    services = Service.objects.all()
    return render(request, 'dashboard/services.html', {'services': services})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/service_form.html', {'form': form})

@login_required
def service_update(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'dashboard/service_form.html', {'form': form})

@login_required
def service_delete(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect('services')
    return render(request, 'dashboard/service_confirm_delete.html', {'service': service})

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)  # Save the form but don't commit yet

            # Get the selected User (doctor) from the form data
            selected_doctor_user = form.cleaned_data['doctor']  # This is a User instance

            # Now find the corresponding Doctor instance
            doctor_instance = get_object_or_404(User, id=selected_doctor_user.id)

            # Assign the Doctor instance to the appointment
            appointment.doctor = doctor_instance
            appointment.client = request.user
            # Now save the appointment to the database
            appointment.save()

            return redirect('homepage')  # Redirect to the homepage or another page after saving
    else:
        form = AppointmentForm()

    return render(request, 'dashboard/make_appointment.html', {'form': form})

@login_required
def appointment_detail(request):
    appointment = Appointment.objects.all()
    return render(request, 'dashboard/appointment.html', {'appointments': appointment})

@login_required
def update_appointment(request, appointmentid):
    appointment = Appointment.objects.get(id=appointmentid)
    if request.method == 'POST':
        status = request.POST.get('status')
        appointment.appointment_status = status
        appointment.save()
        # Redirect back to the same page after updating
        return redirect('update_appointment', appointmentid=appointmentid)

    return redirect('appointment_detail')

@login_required
def home_view(request):
    return render(request, 'dashboard/homepage.html')

@login_required
def appointment_report(request, appointment_id):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        appointments = Appointment.objects.filter(appointment_date__range=[parse_date(start_date), parse_date(end_date)])
    else:
        appointments = Appointment.objects.all()

    total_appointments = appointments.count()

    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'dashboard/report.html', context)

@login_required
def appointment_detail_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {'appointment': appointment}
    return render(request, 'dashboard/appointment_report.html', context)

@login_required
def delete_appointment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return redirect('appointment_detail') 
