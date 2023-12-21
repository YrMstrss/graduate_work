from django.contrib import admin

from content.models import Publication, Likes, Dislikes


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'publication_date', )


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'publication', 'is_active')


@admin.register(Dislikes)
class DislikesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'publication', 'is_active')
