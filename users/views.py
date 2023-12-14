from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileChangeForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class UserSubscribeView(View):
    def get(self, request, pk):
        author = User.objects.get(pk=pk)
        user = self.request.user

        if author in user.subscriptions.all():
            user.subscriptions.remove(author)
        else:
            user.subscriptions.add(author)

        return redirect('users:profile')
