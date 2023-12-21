from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from content.forms import PublicationForm
from content.models import Publication, Likes, Dislikes


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        obj = self.get_object()
        try:
            like = Likes.objects.get(user=user, publication=obj)

            if like.is_active:
                context['is_liked'] = True
            else:
                context['is_liked'] = False

        except ObjectDoesNotExist:
            context['is_liked'] = False

        try:
            dislike = Dislikes.objects.get(user=user, publication=obj)

            if dislike.is_active:
                context['is_disliked'] = True
            else:
                context['is_disliked'] = False

        except ObjectDoesNotExist:
            context['is_disliked'] = False

        return context


class PublicationUpdateView(UpdateView):
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')


class SetLikeView(View):
    def get(self, request, pk):
        post = Publication.objects.get(pk=pk)
        user = request.user
        try:
            like = Likes.objects.get(user=user, publication=post)

            if like.is_active:
                like.is_active = False
                like.save()
            else:
                like.is_active = True
                like.save()

        except ObjectDoesNotExist:
            Likes.objects.create(
                user=user,
                publication=post,
                is_active=True
            )

        return redirect(reverse_lazy('publication:publication-detail', args=[post.pk]))

class SetDislikeView(View):
    def get(self, request, pk):
        post = Publication.objects.get(pk=pk)
        user = request.user
        try:
            dislike = Dislikes.objects.get(user=user, publication=post)

            if dislike.is_active:
                dislike.is_active = False
                dislike.save()
            else:
                dislike.is_active = True
                dislike.save()

        except ObjectDoesNotExist:
            Dislikes.objects.create(
                user=user,
                publication=post,
                is_active=True
            )

        return redirect(reverse_lazy('publication:publication-detail', args=[post.pk]))
