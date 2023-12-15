from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

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


class PublicationDetailView(DetailView):
    model = Publication

    def get_object(self, queryset=None):

        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()

        return self.object


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')
