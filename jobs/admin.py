from django.contrib import admin
from .models import Profile, Company, Job, Application

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone', 'bio')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location', 'contact_email', 'website')
    search_fields = ('company_name', 'location', 'contact_email', 'user__username')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'category', 'salary', 'deadline', 'is_active')
    list_filter = ('is_active', 'job_type', 'category', 'deadline')
    search_fields = ('title', 'company__company_name', 'location', 'description')
    date_hierarchy = 'posted_date'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'applied_date', 'status')
    list_filter = ('status', 'applied_date')
    search_fields = ('applicant__username', 'applicant__email', 'job__title', 'job__company__company_name')
    readonly_fields = ('applied_date',)
