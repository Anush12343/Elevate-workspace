from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Company, Job, Application

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('company_admin', 'Company Admin (Employer)'),
    ]
    
    email = forms.EmailField(required=True, help_text="Required for communication.")
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.RadioSelect, initial='job_seeker')
    phone = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    # Company details (conditionally required if role is company_admin)
    company_name = forms.CharField(max_length=200, required=False, label="Company Name")
    company_location = forms.CharField(max_length=200, required=False, label="Company Location")
    company_email = forms.EmailField(required=False, label="Company Contact Email")
    company_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Company Description")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'company_admin':
            company_name = cleaned_data.get('company_name')
            company_location = cleaned_data.get('company_location')
            company_email = cleaned_data.get('company_email')
            
            if not company_name:
                self.add_error('company_name', 'Company Name is required for Company Admin registration.')
            if not company_location:
                self.add_error('company_location', 'Company Location is required for Company Admin registration.')
            if not company_email:
                self.add_error('company_email', 'Company Contact Email is required.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        role = self.cleaned_data.get('role')
        
        # Access or update the automatically created profile from signal
        profile = user.profile
        profile.role = role
        profile.phone = self.cleaned_data.get('phone')
        profile.bio = self.cleaned_data.get('bio')
        profile.save()
        
        if role == 'company_admin':
            Company.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                location=self.cleaned_data.get('company_location'),
                contact_email=self.cleaned_data.get('company_email'),
                description=self.cleaned_data.get('company_description', '')
            )
            
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'category', 'location', 'salary', 'deadline', 'description', 'requirements', 'is_active']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Profile
        fields = ['phone', 'bio', 'resume']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return profile

class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'contact_email', 'location', 'website', 'description', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
