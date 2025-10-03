from datetime import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz
from jobtracker.core.models import User, TimeStampedModel
from celery.app.control import Control
from jobtracker.celery import app as celery_app
from jobtracker.applications.tasks import send_reminder_mail

class JobApplication(TimeStampedModel):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    job_url = models.URLField()
    platform = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date_applied = models.DateField()
    notes = models.TextField(blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.company} - {self.role}"

@receiver(post_save, sender=JobApplication)
def _post_save_receiver(sender, instance, created, **kwargs):
    if instance.follow_up_date:
        reminder, _ = Reminder.objects.update_or_create(
            application = instance,
            defaults={
                "user": instance.user,
                "remind_at": instance.follow_up_date,
                "message": f"Follow up for {instance.role} at {instance.company}"
            }
        )

    else:
        Reminder.objects.filter(job_application=instance).delete()

class Reminder(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=255)
    remind_at = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    celery_task_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Reminder for {self.user.email} at {self.remind_at}'


@receiver(post_save, sender=Reminder)
def _post_save_receiver(sender, instance, created, **kwargs):
    from django.utils.timezone import now
    import pytz
    utc = pytz.UTC
    if instance.pk:
        old = Reminder.objects.get(pk=instance.pk)
        if old.celery_task_id:
            try:
                Control(app=celery_app).revoke(old.celery_task_id, terminate=True)
            except Exception:
                pass

    if instance.remind_at:
        eta = instance.remind_at
        if eta > now():
            result = send_reminder_mail.apply_async(
                args=[instance.id],
                eta=eta
            )
            Reminder.objects.filter(pk=instance.pk).update(celery_task_id=result.id)