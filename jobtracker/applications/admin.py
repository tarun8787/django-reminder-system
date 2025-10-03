from django.contrib import admin
from jobtracker.applications.models import JobApplication, Reminder

# Register your models here.
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display=('id', 'get_user_email', 'company', 'role', 'modified_at')
    raw_id_fields=('user',)

    def get_user_email(self, obj):
        return obj.user
    

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display=('id', 'get_user_email', 'get_job_application', 'remind_at', 'modified_at')
    raw_id_fields=('user', 'application')

    def get_user_email(self, obj):
        return obj.user
        
    def get_job_application(self, obj):
        return obj.application