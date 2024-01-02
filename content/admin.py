from django.contrib import admin

from content.models import Publication, Like, Dislike


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'publication_date', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'publication', 'is_active')


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'publication', 'is_active')
