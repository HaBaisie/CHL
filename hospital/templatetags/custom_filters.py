from django import template
from django.contrib.auth.models import User
from hospital.models import Doctor

register = template.Library()

@register.filter
def get_doctor_name(doctor_id):
    """Return the full name of a doctor given their ID."""
    if not doctor_id:
        return "N/A"
    try:
        doctor = Doctor.objects.select_related('user').get(id=doctor_id)
        return f"{doctor.user.first_name} {doctor.user.last_name}"
    except Doctor.DoesNotExist:
        return "Unknown Doctor"