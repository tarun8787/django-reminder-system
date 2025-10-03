from django.contrib import admin

# Register your models here.
from jobtracker.core.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id', 'email', 'username')