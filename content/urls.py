from django.urls import path

from content.apps import ContentConfig
from content.views import PublicationCreateView, PublicationListView, PublicationUpdateView, PublicationDetailView, \
    SetLikeView, SetDislikeView, SearchListView

app_name = ContentConfig.name

urlpatterns = [
    path('create/', PublicationCreateView.as_view(), name='create-publication'),
    path('', PublicationListView.as_view(), name='list-publications'),
    path('update/<int:pk>/', PublicationUpdateView.as_view(), name='update-publication'),
    path('<int:pk>/', PublicationDetailView.as_view(), name='publication-detail'),

    path('like/<int:pk>/', SetLikeView.as_view(), name='set-like'),
    path('dislike/<int:pk>/', SetDislikeView.as_view(), name='set-dislike'),
    path('search-results', SearchListView.as_view(), name='search'),
]
