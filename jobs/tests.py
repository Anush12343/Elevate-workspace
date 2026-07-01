from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from .models import Profile, Company, Job, Application

class JobPortalTests(TestCase):
    def setUp(self):
        # Create Job Seeker User
        self.seeker_user = User.objects.create_user(username='seeker', password='password123', email='seeker@test.com')
        # Profile is created via signals automatically. Ensure it is job_seeker.
        self.seeker_user.profile.role = 'job_seeker'
        self.seeker_user.profile.save()
        
        # Create Company Admin User
        self.employer_user = User.objects.create_user(username='employer', password='password123', email='employer@test.com')
        self.employer_user.profile.role = 'company_admin'
        self.employer_user.profile.save()
        # Create a Company associated with employer
        self.company = Company.objects.create(
            user=self.employer_user,
            company_name="Elevate Test Company",
            description="Leading test company in Nepal",
            location="Kathmandu",
            contact_email="test@elevate.com.np"
        )
        
        # Create a Job
        self.job = Job.objects.create(
            company=self.company,
            title="Django Developer",
            description="Write clean code",
            requirements="Python & Django expertise",
            salary=85000,
            location="Kathmandu",
            deadline=date(2026, 12, 31),
            job_type="Full-time",
            category="IT & Software"
        )

    def test_profile_auto_creation_signal(self):
        """Test that Profile is automatically created on User creation."""
        user = User.objects.create_user(username='new_user', password='password123')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.role, 'job_seeker')

    def test_job_seeker_dashboard_access(self):
        """Test that Job Seekers can access Seeker Dashboard and Company Admins are denied."""
        self.client.login(username='seeker', password='password123')
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username='employer', password='password123')
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirects to home due to role-check decorator

    def test_employer_job_creation(self):
        """Test that Company Admins can create jobs, but Job Seekers cannot."""
        # Seeker fails
        self.client.login(username='seeker', password='password123')
        response = self.client.post(reverse('job_create'), {
            'title': 'Junior Python Developer',
            'job_type': 'Full-time',
            'category': 'IT & Software',
            'location': 'Pokhara',
            'salary': 45000,
            'deadline': '2026-11-30',
            'description': 'Help write code',
            'requirements': 'Basic Python skills',
            'is_active': True
        })
        self.assertEqual(response.status_code, 302) # Denied and redirected
        self.assertFalse(Job.objects.filter(title='Junior Python Developer').exists())
        
        # Employer succeeds
        self.client.login(username='employer', password='password123')
        response = self.client.post(reverse('job_create'), {
            'title': 'Junior Python Developer',
            'job_type': 'Full-time',
            'category': 'IT & Software',
            'location': 'Pokhara',
            'salary': 45000,
            'deadline': '2026-11-30',
            'description': 'Help write code',
            'requirements': 'Basic Python skills',
            'is_active': True
        })
        self.assertEqual(response.status_code, 302) # Redirected to company dashboard
        self.assertTrue(Job.objects.filter(title='Junior Python Developer').exists())

    def test_job_application_flow(self):
        """Test that Job Seekers can apply for a job and upload their CV."""
        self.client.login(username='seeker', password='password123')
        
        # Create a mock file
        cv_file = SimpleUploadedFile("my_resume.pdf", b"file_content", content_type="application/pdf")
        
        response = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'cover_letter': 'I love coding in Python!',
            'cv': cv_file
        })
        self.assertEqual(response.status_code, 302) # Redirects to user dashboard
        self.assertTrue(Application.objects.filter(job=self.job, applicant=self.seeker_user).exists())
