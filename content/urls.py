from django.urls import path

from content.apps import ContentConfig
from content.views import HomePage

app_name = ContentConfig.name

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]
