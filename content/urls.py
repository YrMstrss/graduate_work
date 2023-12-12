from django.urls import path

from content.apps import ContentConfig
from content.views import PublicationCreateView

app_name = ContentConfig.name

urlpatterns = [
    path('create/', PublicationCreateView.as_view(), name='create-publication'),
]
