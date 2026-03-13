from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'message')