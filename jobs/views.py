from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Company, Job, Application, Profile
from .forms import UserRegistrationForm, JobForm, ProfileEditForm, CompanyEditForm
from .decorators import company_admin_required, job_seeker_required
from .services import generate_random_job, get_or_create_company_for_user

def home(request):
    featured_jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:3]
    stats = {
        'jobs_count': Job.objects.filter(is_active=True).count(),
        'companies_count': Company.objects.count(),
        'applications_count': Application.objects.count(),
    }
    return render(request, 'home.html', {'featured_jobs': featured_jobs, 'stats': stats})

def job_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')
    category = request.GET.get('category', '')
    
    jobs = Job.objects.filter(is_active=True)
    
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(requirements__icontains=query))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if category:
        jobs = jobs.filter(category=category)
        
    jobs = jobs.order_by('-posted_date')
    
    # Pagination (6 jobs per page)
    paginator = Paginator(jobs, 6)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)
    
    context = {
        'jobs': jobs_page,
        'query': query,
        'location': location,
        'job_type': job_type,
        'category': category,
        'categories': Job.CATEGORIES,
        'job_types': Job.JOB_TYPES,
    }
    return render(request, 'job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
@job_seeker_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job_id=job.id)
        
    if request.method == 'POST':
        cv = request.FILES.get('cv')
        cover_letter = request.POST.get('cover_letter', '')
        
        # Fallback to profile resume if CV is not uploaded
        if not cv and request.user.profile.resume:
            cv = request.user.profile.resume
            
        if not cv:
            messages.error(request, "Please upload a CV or add a resume to your profile first.")
            return render(request, 'apply_job.html', {'job': job})
            
        Application.objects.create(
            job=job,
            applicant=request.user,
            cv=cv,
            cover_letter=cover_letter
        )
        messages.success(request, 'Your application was submitted successfully!')
        return redirect('user_dashboard')
        
    return render(request, 'apply_job.html', {'job': job})

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Elevate Workforce Solutions.')
            return redirect('dashboard_redirect')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'next': request.GET.get('next', '')})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

# Unified redirection view based on role
@login_required
def dashboard_redirect(request):
    # Admin or staff should see the company dashboard
    if request.user.is_staff or request.user.is_superuser:
        return redirect('company_dashboard')
    # Fallback to role-based profile check
    if hasattr(request.user, 'profile') and request.user.profile.role == 'company_admin':
        return redirect('company_dashboard')
    return redirect('user_dashboard')

# Job Seeker Dashboard & Profile management
@login_required
@job_seeker_required
def user_dashboard(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_date')
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
        
    context = {
        'applications': applications,
        'form': form,
    }
    return render(request, 'user_dashboard.html', context)

# Company Dashboard & Management
@login_required
@company_admin_required
def company_dashboard(request):
    # Ensure a Company instance exists for the admin user
    company = get_or_create_company_for_user(request.user)
    jobs = company.jobs.all().order_by('-posted_date')
    
    # Calculate stats
    total_jobs = jobs.count()
    total_applications = Application.objects.filter(job__company=company).count()
    pending_applications = Application.objects.filter(job__company=company, status='pending').count()
    
    if request.method == 'POST':
        form = CompanyEditForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company details updated successfully!')
            return redirect('company_dashboard')
    else:
        form = CompanyEditForm(instance=company)
        
    context = {
        'company': company,
        'jobs': jobs,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'form': form,
    }
    return render(request, 'company_dashboard.html', context)

# Company Job CRUD operations
@login_required
@company_admin_required
def job_create(request):
    company = get_or_create_company_for_user(request.user)
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, f'Job listing "{job.title}" created successfully!')
            return redirect('company_dashboard')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {'form': form, 'title': 'Create New Job Listing'})

@login_required
@company_admin_required
def job_update(request, job_id):
    company = get_or_create_company_for_user(request.user)
    job = get_object_or_404(Job, id=job_id, company=company)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f'Job listing "{job.title}" updated successfully!')
            return redirect('company_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form, 'job': job, 'title': 'Edit Job Listing'})

@login_required
@company_admin_required
def job_delete(request, job_id):
    """Delete a job listing (POST only)."""
    if request.method != 'POST':
        messages.error(request, "Invalid request method for deleting a job.")
        return redirect('company_dashboard')
    company = get_or_create_company_for_user(request.user)
    job = get_object_or_404(Job, id=job_id, company=company)
    job_title = job.title
    job.delete()
    messages.success(request, f'Job listing "{job_title}" was deleted.')
    return redirect('company_dashboard')

# View applicants for a specific job

@login_required
@company_admin_required
def random_job(request):
    """Generate a random job (demo) and redirect to dashboard."""
    generate_random_job(created_by=request.user)
    messages.success(request, "Random demo job created successfully!")
    return redirect('company_dashboard')
@login_required
@company_admin_required
def view_applicants(request, job_id):
    company = get_or_create_company_for_user(request.user)
    job = get_object_or_404(Job, id=job_id, company=company)
    applications = job.applications.all().order_by('-applied_date')
    
    return render(request, 'view_applicants.html', {'job': job, 'applications': applications})

# Update application status
@login_required
@company_admin_required
def update_application_status(request, app_id):
    company = get_or_create_company_for_user(request.user)
    application = get_object_or_404(Application, id=app_id, job__company=company)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'reviewed', 'accepted', 'rejected']:
            application.status = status
            application.save()
            messages.success(request, f"Status of {application.applicant.username}'s application updated to {status.capitalize()}.")
        else:
            messages.error(request, "Invalid status choice.")
            
    return redirect('view_applicants', job_id=application.job.id)
