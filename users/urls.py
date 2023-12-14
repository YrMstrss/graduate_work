from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, UserSubscribeView, SubscriptionListView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('subscribe/<int:pk>/', UserSubscribeView.as_view(), name='subscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscriptions-list'),

]
