from django.contrib import admin

from content.models import Publication, Likes


@admin.register(Publication)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'publication_date', )


@admin.register(Likes)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'publication', 'is_active')
