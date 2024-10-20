from django import forms
from .models import Appointment, Doctor, Service, User, Admin
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Appointment, User, Service

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Password')
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')

    class Meta:
        model = User
        fields = ['identitycardno', 'username', 'fullname', 'email', 'phone_no', 'address', 'role', 'password', 'new_password']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(UserForm, self).__init__(*args, **kwargs)

        if instance and instance.role == User.ADMIN:
            self.fields['position'] = forms.CharField(max_length=255, label="Position", required=True)
        
        elif instance and instance.role == User.DOCTOR:
            self.fields['specialization'] = forms.CharField(max_length=255, label="Specialization", required=True)
            self.fields['qualification'] = forms.CharField(max_length=255, label="Qualification", required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')

        if not self.instance.pk and not password:
            self.add_error('password', 'Password is required for new users.')

        if new_password and len(new_password) < 8:
            self.add_error('new_password', 'New password must be at least 8 characters long.')

        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'service_type', 'service_detail']

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}))
    
    # Filter users who are doctors (role=1)
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.DOCTOR),
        label="Select Doctor",
        empty_label="Choose a doctor",
        to_field_name="fullname",  # Reference the fullname attribute in User model
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label="Select Service",
        empty_label="Choose a service",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'date', 'time']


