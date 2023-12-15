from django.contrib import admin

from content.models import Publication


@admin.register(Publication)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'publication_date', )
