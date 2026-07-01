import random
import string
from datetime import date, timedelta

from .models import Company, Job


def get_or_create_company_for_user(user):
    return Company.objects.get_or_create(
        user=user,
        defaults={
            'company_name': f"{user.username}'s Company",
            'description': 'Auto-generated company profile. Update this from your dashboard.',
            'location': 'Unknown',
            'contact_email': user.email or 'admin@example.com',
        },
    )[0]


def _random_string(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_job(created_by):
    company = get_or_create_company_for_user(created_by)

    title = f"{random.choice(['Senior', 'Junior', 'Lead', 'Assistant'])} "
    title += f"{random.choice(['Developer', 'Engineer', 'Analyst', 'Designer'])} "
    title += _random_string(4)

    job = Job.objects.create(
        company=company,
        title=title,
        description=(
            "This is a demo job generated automatically for testing the UI. "
            "It includes placeholder responsibilities and requirements."
        ),
        requirements="- Requirement 1\n- Requirement 2\n- Requirement 3",
        salary=random.randint(50000, 150000),
        location=random.choice(['Kathmandu', 'Pokhara', 'Remote']),
        deadline=date.today() + timedelta(days=random.randint(30, 90)),
        job_type=random.choice([choice[0] for choice in Job.JOB_TYPES]),
        category=random.choice([choice[0] for choice in Job.CATEGORIES]),
    )
    return job
