from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_notification(course_title: str, email: str) -> None:
    """
    Sends notification to the subscriber of the course
    """
    send_mail(
        subject='Course Updated',
        message=f'Hi!\n\nCourse {course_title} has been updated.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

