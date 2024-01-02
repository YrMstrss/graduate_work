from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView

from content.forms import PublicationForm
from content.models import Publication, Like, Dislike
from content.services import toggle_like, toggle_dislike, create_like, create_dislike
from users.models import User


class HomePage(TemplateView):
    """
    Контроллер для вывода домашней страницы
    """
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        """
        Получение контекстной информации
        :param kwargs:
        :return: Контекстная информация
        """
        context = super().get_context_data(**kwargs)

        users = User.objects.all()
        the_most_popular_author = None
        prev_subscriber_counter = 0
        for author in users:
            subscriber_counter = 0
            for user in users:
                if author in user.subscriptions.all():
                    subscriber_counter += 1
            if subscriber_counter > prev_subscriber_counter:
                prev_subscriber_counter = subscriber_counter
                the_most_popular_author = author
        context['the_most_popular_author'] = the_most_popular_author

        the_most_popular_post = Publication.objects.order_by('-views')
        context['the_most_popular_post'] = the_most_popular_post[0]

        return context


class NoPermPage(TemplateView):
    """
    Контроллер для вывода страницы с информацией, о том, что у пользователя не хватает прав на какое-то действие
    """
    template_name = 'content/have_no_permission.html'


class PublicationCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер для создания публикации
    """
    model = Publication
    form_class = PublicationForm
    success_url = reverse_lazy('home')
    raise_exception = False

    def form_valid(self, form):
        """
        Проверка валидности формы и запись текущего пользователя в поле автора публикации
        :param form: Форма для создания публикации
        :return: Проверка валидности формы
        """
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()

        return super().form_valid(form)


class PublicationListView(ListView):
    """
    Контроллер вывода списка публикаций
    """
    model = Publication
    context_object_name = 'posts'


class PublicationDetailView(DetailView):
    """
    Контроллер вывода конкретной записи
    """
    model = Publication
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """
        Получает объект публикации и добавляет 1 к счетчику просмотров при переходе на страницу публикации
        :param queryset: None
        :return: Публикация
        """

        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()

        return self.object

    def get_context_data(self, **kwargs):
        """
        Получение контекстной информации на странице объекта
        :param kwargs:
        :return: Контекстная информация (счетчик лайков и дизлайков, информацию о том, лайкнул/дизлайкнул ли
        пользователь запись)
        """
        context = super().get_context_data()
        user = self.request.user
        if user.pk is None:
            return context
        obj = self.get_object()
        try:
            like = Like.objects.get(user=user, publication=obj)

            if like.is_active:
                context['is_liked'] = True
            else:
                context['is_liked'] = False

        except ObjectDoesNotExist:
            context['is_liked'] = False

        try:
            dislike = Dislike.objects.get(user=user, publication=obj)

            if dislike.is_active:
                context['is_disliked'] = True
            else:
                context['is_disliked'] = False

        except ObjectDoesNotExist:
            context['is_disliked'] = False

        like_counter = Like.objects.filter(publication=obj, is_active=True).count()
        dislike_counter = Dislike.objects.filter(publication=obj, is_active=True).count()

        context['like_counter'] = like_counter
        context['dislike_counter'] = dislike_counter

        return context


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для редактирования публикации
    """
    model = Publication
    form_class = PublicationForm

    def get(self, request, *args, **kwargs):
        """
        Проверяет, является ли текущий пользователь автором публикации
        :param request:
        :param args:
        :param kwargs:
        :return: Редирект на страницу с информацией о тои, что пользователь не может совершить данное действие
        """
        if request.user == self.get_object().author:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('no-perm'))

    def get_success_url(self):
        """
        Получает ссылку для перенаправления пользователя на страницу публикации после успешного редактирования поста
        :return: Ссылка на страницу публикации
        """
        return reverse_lazy('publication:publication-detail', args=[self.object.pk])


class SetLikeView(LoginRequiredMixin, View):
    """
    Контроллер, чтобы поставить лайк
    """
    def get(self, request, pk):
        """
        Проверяет существования объекта лайка для заданной публикации от текущего пользователя. При его отсутствии
        создает его, при его существовании изменяет поле активности лайка
        :param request:
        :param pk: ID записи
        :return: Редирект на предыдущую страницу
        """
        post = Publication.objects.get(pk=pk)
        user = request.user
        try:
            like = Like.objects.get(user=user, publication=post)

            try:
                dislike = Dislike.objects.get(user=user, publication=post)
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
                dislike = Dislike.objects.get(user=user, publication=post)
                if dislike.is_active:
                    dislike.is_active = False
                    dislike.save()
                    create_like(user, post)
                else:
                    create_like(user, post)
            except ObjectDoesNotExist:
                create_like(user, post)

        return redirect(request.META.get('HTTP_REFERER'))


class SetDislikeView(LoginRequiredMixin, View):
    """
    Контроллер, чтобы поставить дизлайк
    """
    def get(self, request, pk):
        """
        Проверяет существования объекта дизлайка для заданной публикации от текущего пользователя. При его отсутствии
        создает его, при его существовании изменяет поле активности дизлайка
        :param request:
        :param pk: ID записи
        :return: Редирект на предыдущую страницу
        """
        post = Publication.objects.get(pk=pk)
        user = request.user
        try:
            dislike = Dislike.objects.get(user=user, publication=post)

            try:
                like = Like.objects.get(user=user, publication=post)

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
                like = Like.objects.get(user=user, publication=post)

                if like.is_active:
                    like.is_active = False
                    like.save()
                    create_dislike(user, post)
                else:
                    create_dislike(user, post)
            except ObjectDoesNotExist:
                create_dislike(user, post)

        return redirect(request.META.get('HTTP_REFERER'))


class SearchListView(ListView):
    """
    Контроллер поисковой строки
    """
    model = Publication
    template_name = 'content/publication_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Получает все записи в названии или содержании которых есть запрос из поисковой строки
        :return: Список подходящих записей
        """
        query = self.request.GET.get('q')
        object_list = Publication.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list
