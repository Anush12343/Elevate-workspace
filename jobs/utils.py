# jobs/utils.py
"""Utility functions for the Job Portal app.

This module provides helper functions that are used across the
application. Currently it contains a function to generate a random
job listing for demonstration purposes.
"""

import random
import string
from datetime import date, timedelta
from .models import Company, Job


def _random_string(length=8):
    """Return a random alphanumeric string of `length` characters."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_job(created_by):
    """Create a random job linked to `created_by`'s Company.

    - If the user does not have an associated ``Company`` instance it
      will be created automatically (similar to the logic in
      ``company_dashboard``).
    - The job fields are populated with placeholder data that satisfies
      model constraints.
    - The function returns the newly created ``Job`` object.
    """
    # Ensure a Company exists for the user
    company, _ = Company.objects.get_or_create(
        user=created_by,
        defaults={
            'company_name': f"{created_by.username}'s Company",
            'description': 'Auto-generated company for demo purposes.',
            'location': 'Unknown',
            'contact_email': created_by.email or 'admin@example.com',
        },
    )

    # Generate dummy data for the job
    title = f"{random.choice(['Senior', 'Junior', 'Lead', 'Assistant'])} " 
    title += f"{random.choice(['Developer', 'Engineer', 'Analyst', 'Designer'])} "
    title += _random_string(4)

    description = "This is a demo job generated automatically for testing the UI. "
    description += "It includes placeholder responsibilities and requirements."
    requirements = "- Requirement 1\n- Requirement 2\n- Requirement 3"
    salary = random.randint(50000, 150000)
    location = random.choice(['Kathmandu', 'Pokhara', 'Remote'])
    deadline = date.today() + timedelta(days=random.randint(30, 90))
    job_type = random.choice([choice[0] for choice in Job.JOB_TYPES])
    category = random.choice([choice[0] for choice in Job.CATEGORIES])

    job = Job.objects.create(
        company=company,
        title=title,
        description=description,
        requirements=requirements,
        salary=salary,
        location=location,
        deadline=deadline,
        job_type=job_type,
        category=category,
    )
    return job
