from rest_framework import viewsets, permissions
from jobtracker.applications.models import JobApplication, Reminder
from jobtracker.applications.serializers import JobApplicationSerializer, ReminderSerializer
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class JobApplicationViewSet(viewsets.ModelViewSet):
    model = JobApplication
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_filter(self, *args, **kwargs):
        query_dict = {
            key: value
            for key, value in kwargs.items() if value
        }
        logger.debug(f"Filtering JobApplications with {query_dict}")
        return query_dict

    def get_queryset(self, *args, **kwargs):
        query_filter = self.get_filter(**kwargs)
        return self.model.objects.filter(**query_filter)

    def list(self, request):
        user = request.user
        logger.info(f"User {user} requested job applications list")
        job_application_qs =self.get_queryset(user = user)
        serializer = self.serializer_class(instance = job_application_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        user = request.user
        try:
            job_application_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"JobApplication with id={pk} not found for user {user}")
            return Response({"detail": "Job Application not found"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"User {user} retrieved JobApplication {pk}")
        serializer = self.serializer_class(instance = job_application_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        logger.info(f"User {request.user} is creating a JobApplication")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.debug(f"JobApplication created: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"JobApplication creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            job_application_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"JobApplication with id={pk} not found for update")
            return Response({"detail": "Job Application not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=job_application_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"JobApplication {pk} updated")
            return Response(serializer.data)
        
        logger.error(f"JobApplication update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            job_application_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"JobApplication with id={pk} not found for deletion")
            return Response({"detail": "Job Application not found"}, status=status.HTTP_404_NOT_FOUND)

        job_application_obj.delete()
        logger.info(f"JobApplication {pk} deleted by user {request.user}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReminderViewSet(viewsets.ModelViewSet):
    model = Reminder
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_filter(self, *args, **kwargs):
        query_dict = {
            key: value
            for key, value in kwargs.items() if value
        }

        return query_dict

    def get_queryset(self, *args, **kwargs):
        query_filter = self.get_filter(**kwargs)
        logger.debug(f"Filtering Reminders with {query_filter}")
        return self.model.objects.filter(**query_filter)

    def list(self, request):
        user = request.user
        logger.info(f"User {user} requested reminder list")
        reminder_qs =self.get_queryset(user = user)
        serializer = self.serializer_class(instance = reminder_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            reminder_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"Reminder with id={pk} not found")
            return Response({"detail": "Reminder not found"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"User {request.user} retrieved Reminder {pk}")
        serializer = self.serializer_class(instance = reminder_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        logger.info(f"User {request.user} is creating a Reminder")
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            logger.debug(f"Reminder created: {serializer.data}")
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"Reminder creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            reminder_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"Reminder with id={pk} not found for update")
            return Response({"detail": "Reminder not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=reminder_obj, data=request.data, partial=True)
        if serializer.is_valid():
            logger.info(f"Reminder {pk} updated")
            serializer.save()
            return Response(serializer.data)
        
        logger.error(f"Reminder update failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            reminder_obj = self.get_queryset(user=request.user).get(id=pk)
        except self.model.DoesNotExist:
            logger.warning(f"Reminder with id={pk} not found for deletion")
            return Response({"detail": "Reminder not found"}, status=status.HTTP_404_NOT_FOUND)

        reminder_obj.delete()
        logger.info(f"Reminder {pk} deleted by user {request.user}")
        return Response(status=status.HTTP_204_NO_CONTENT)