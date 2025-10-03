from django.apps import AppConfig
from django.utils.timezone import now


class ApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobtracker.applications'
    verbose_name='applications'

    def ready(self):
        from jobtracker.applications.models import Reminder
        from jobtracker.applications.tasks import send_reminder_mail

        future_reminders = Reminder.objects.filter(remind_at__gt=now())
        for reminder in future_reminders:
            try:
                result = send_reminder_mail.apply_async(
                    args=[reminder.id],
                    eta=reminder.remind_at
                )
                reminder.celery_task_id = result.id
                reminder.save(update_fields=["celery_task_id"])
                print(f"Rescheduled reminder {reminder.id}")
            except Exception as e:
                print(f"Failed to reschedule reminder {reminder.id}: {e}")

