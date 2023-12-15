from django.urls import path

from content.apps import ContentConfig
from content.views import PublicationCreateView, PublicationListView, PublicationUpdateView, PublicationDetailView

app_name = ContentConfig.name

urlpatterns = [
    path('create/', PublicationCreateView.as_view(), name='create-publication'),
    path('', PublicationListView.as_view(), name='list-publications'),
    path('update/<int:pk>/', PublicationUpdateView.as_view(), name='update-publication'),
    path('<int:pk>/', PublicationDetailView.as_view(), name='publication-detail'),
]
