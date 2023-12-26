from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from content.views import HomePage, NoPermPage
from users.views import CreateCheckoutSession

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('publication/', include('content.urls', namespace='publication')),
    path('user/', include('users.urls', namespace='user')),
    path('no-permission/', NoPermPage.as_view(), name='no-perm'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSession.as_view(), name='create-checkout-session'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
