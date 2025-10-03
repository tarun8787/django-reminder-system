import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_mail(reminder_id):
    from jobtracker.applications.models import Reminder

    logger.info(f"Executing task: Sending reminder for ID: {reminder_id}")

    try:
        reminder_obj = Reminder.objects.get(id=reminder_id)

        if reminder_obj.is_sent:
            logger.warning(f"Reminder {reminder_id} already sent.")
            return 'Already sent'
        

        send_mail(
            subject="Your Scheduled Reminder",
            message=reminder_obj.message or "Reminder message not set",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[reminder_obj.user.email],
            fail_silently=False
        )

        reminder_obj.is_sent = True
        reminder_obj.save()

        logger.info(f"Email successfully sent to {reminder_obj.user.email}")
        return f"Sent to {reminder_obj.user.email}"

    except Reminder.DoesNotExist:
        logger.error(f"Reminder with ID {reminder_id} does not exist.")
        return 'Reminder Not Found'

    except Exception as e:
        logger.exception(f"Error while sending reminder for ID {reminder_id}: {e}")
        return str(e)
