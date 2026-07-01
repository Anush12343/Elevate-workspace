from .models import Company


def user_context(request):
    user = getattr(request, 'user', None)
    profile = None
    company = None
    role = None
    resume = None

    if user and user.is_authenticated and hasattr(user, 'profile'):
        profile = user.profile
        role = profile.role
        resume = profile.resume
        if role == 'company_admin':
            company = Company.objects.filter(user=user).first()

    return {
        'user_profile': profile,
        'user_role': role,
        'user_resume': resume,
        'user_company': company,
    }
