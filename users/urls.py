from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileUpdateView, UserSubscribeView, SubscriptionListView, ProfileDetailView, \
    OwnProfileDetailView, Login, SubscribeInfoView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', Login.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile-view'),
    path('subscribe/<int:pk>/', UserSubscribeView.as_view(), name='subscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscriptions-list'),
    path('my-profile', OwnProfileDetailView.as_view(), name='my-profile'),
    path('subscribe-info/<int:pk>', SubscribeInfoView.as_view(), name='subscribe-info'),

]
