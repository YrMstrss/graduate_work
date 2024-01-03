from django.contrib import admin

from users.models import User


@admin.register(User)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'phone', 'email')
