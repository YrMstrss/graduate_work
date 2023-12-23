from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from content.forms import PublicationForm
from content.models import Publication, Likes, Dislikes
from content.services import toggle_like, toggle_dislike, create_like, create_dislikes


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
    context_object_name = 'posts'


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

        like_counter = Likes.objects.filter(publication=obj, is_active=True).count()
        dislike_counter = Dislikes.objects.filter(publication=obj,is_active=True).count()

        context['like_counter'] = like_counter
        context['dislike_counter'] = dislike_counter

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

            try:
                dislike = Dislikes.objects.get(user=user, publication=post)
                if dislike.is_active:
                    dislike.is_active = False
                    dislike.save()
                    like.is_active = True
                    like.save()
                else:
                    toggle_like(like)

            except ObjectDoesNotExist:

                toggle_like(like)

        except ObjectDoesNotExist:
            try:
                dislike = Dislikes.objects.get(user=user, publication=post)
                if dislike.is_active:
                    dislike.is_active = False
                    dislike.save()
                    create_like(user, post)
                else:
                    create_like(user, post)
            except ObjectDoesNotExist:
                create_like(user, post)

        return redirect(request.META.get('HTTP_REFERER'))


class SetDislikeView(View):
    def get(self, request, pk):
        post = Publication.objects.get(pk=pk)
        user = request.user
        try:
            dislike = Dislikes.objects.get(user=user, publication=post)

            try:
                like = Likes.objects.get(user=user, publication=post)

                if like.is_active:
                    like.is_active = False
                    like.save()
                    dislike.is_active = True
                    dislike.save()
                else:
                    toggle_dislike(dislike)
            except ObjectDoesNotExist:

                toggle_dislike(dislike)

        except ObjectDoesNotExist:
            try:
                like = Likes.objects.get(user=user, publication=post)

                if like.is_active:
                    like.is_active = False
                    like.save()
                    create_dislikes(user, post)
                else:
                    create_dislikes(user, post)
            except ObjectDoesNotExist:
                create_dislikes(user, post)

        return redirect(request.META.get('HTTP_REFERER'))


class SearchListView(ListView):
    model = Publication
    template_name = 'content/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Publication.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list
