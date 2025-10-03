from rest_framework.routers import DefaultRouter
from jobtracker.applications.viewsets import JobApplicationViewSet, ReminderViewSet

application_router = DefaultRouter()

application_router.register(r'job-application', JobApplicationViewSet, basename='job_application'),
application_router.register(r'reminder', ReminderViewSet, basename='reminder'),