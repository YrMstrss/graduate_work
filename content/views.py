from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from content.forms import PublicationForm
from content.models import Publication


class HomePage(TemplateView):
    template_name = 'content/home.html'


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')
