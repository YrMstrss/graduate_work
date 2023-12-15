from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from content.forms import PublicationForm
from content.models import Publication


class HomePage(TemplateView):
    template_name = 'content/home.html'


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class PublicationListView(ListView):
    model = Publication


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')
