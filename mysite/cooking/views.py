from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Post, Comment  # Наши модели
from django.db.models import F, Q
from .forms import PostAddForm, LoginForm, RegisterForm, CommentForm, ChangePasswordForm  # Наши формы
from django.contrib.auth import login, logout  # Для авторизации и выхода из учетки
from django.contrib import messages  # Для реализации информирующих сообщений на сайте
# Импортируем классы для работы с view на основе классов
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from .serializers import PostSerializer, CategorySerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView


# Реализация view на основе классов
class Index(ListView):
    """Отображение главной страницы"""
    model = Post  # Определяем модель, с которой будем работать
    context_object_name = 'posts'  # Указываем имя контекста для шаблонов
    template_name = 'cooking/index.html'  # Указываем шаблон
    extra_context = {'title': 'Главная страница'}   # Указываем контекст с данными, с которыми будем работать в шаблоне


class ArticleByCategory(Index):
    """Реакция на выбор категории"""
    def get_queryset(self):
        """Здесь можем переделать фильтрацию"""
        return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Для динамических данных"""
        contex = super().get_context_data()    # contex = {}
        category = Category.objects.get(pk=self.kwargs['pk'])
        contex['title'] = category
        return contex


class PostDetail(DetailView):
    """Отображение страницы поста"""
    model = Post
    template_name = 'cooking/article_detail.html'

    def get_queryset(self):
        """Делаем дополнительную фильтрацию"""
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()    # contex = {}
        Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)  # Увеличиваем просмотр поста
        post = Post.objects.get(pk=self.kwargs['pk'])
        rec_post = Post.objects.all().exclude(pk=self.kwargs['pk']).order_by('-watched')[:4]
        context['title'] = post
        context['rec_post'] = rec_post
        context['comments'] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm
        return context


class AddPost(CreateView):
    """Добавление статьи от пользователя, без динамики"""
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Добавить статью'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    """Изменение статьи по кнопке"""
    model = Post
    form_class = PostAddForm
    template_name = 'cooking/article_add_form.html'
    extra_context = {'title': 'Изменить статью'}


class PostDelete(DeleteView):
    """Удаление статьи"""
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'


class SearchResult(Index):
    """Поиск слова в заголовках и содержаниях статьи"""

    def get_queryset(self):
        """Функция для фильтрации выборок из БД"""
        word = self.request.GET.get('q')
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


class UserChangePassword(PasswordChangeView):
    """Простой способ смены пароля пользователя"""
    template_name = 'cooking/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('index')


# API
class CookingAPI(ListAPIView):
    """Выдача всех статей по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CookingAPIDetail(RetrieveAPIView):
    """Выдача статьи по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


class CookingCategoryAPI(ListAPIView):
    """Выдача всех категорий по API"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CookingCategoryAPIDetail(RetrieveAPIView):
    """Выдача категории по API"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializer


class SwaggerApiDoc(TemplateView):
    """Документация API"""
    template_name = 'swagger/swagger_ui.html'
    extra_context = {
        'schema_url': 'openapi-schema',
    }


# Реализация view на основе функций

# def index(request):
#     """Отображение главной страницы"""
#     # Определяем модель, с которой будем работать и дастаем из нее вссе данные
#     posts = Post.objects.all()  # SELECT * FROM post
#     context = {   # Указываем контекст с данными, с которыми будем работать в шаблоне
#         'title': 'Главаная страница',
#         'posts': posts,
#     }
#     return render(request, 'cooking/index.html', context)    # Возвращаем шаблон и наш контекст


# def category_list(request, pk):
#     """Реакция на выбор категории"""
#     posts = Post.objects.filter(category_id=pk)  # Отбираем посты по категории
#     context = {
#         'title': posts[0].category,
#         'posts': posts,
#     }
#     return render(request, 'cooking/index.html', context)


# def post_detail(request, pk):
#     """Отображение страницы поста"""
#     articles = Post.objects.get(pk=pk)  # Забираем нужный пост
#     Post.objects.filter(pk=pk).update(watched=F('watched') + 1)  # Увеличиваем просмотр поста
#     # Переменная для вывода постов рекомендаций
#     rec_post = Post.objects.all().exclude(pk=pk).order_by('-watched')[:4]
#     context = {
#         'title': articles.title,
#         'post': articles,
#         'rec_post': rec_post,
#     }
#     return render(request, 'cooking/article_detail.html', context)


# def add_post(request):
#     """Добавление статьи от пользователя, без динамики"""
#     if request.method == 'POST':
#         form = PostAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post.objects.create(**form.cleaned_data)
#             post.save()
#             return redirect('post_detail', post.pk)
#     else:
#         form = PostAddForm()
#
#     context = {
#         'form': form,
#         'title': 'Добавить статью'
#     }
#     return render(request, 'cooking/article_add_form.html', context)


def user_login(request):
    """Аутентификация пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = LoginForm()
    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }
    return render(request, 'cooking/login_form.html', context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')


def user_registrations(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'title': 'Регистрация'
    }
    return render(request, 'cooking/register_form.html', context)


def add_comment(request, post_id):
    """Добавление комментария"""
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен')

    return redirect('post_detail', post_id)


def profile(request, user_id):
    """Страница пользователя"""
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    context = {
        'user': user,
        'posts': posts,
        'title': 'Моя страница',
    }

    return render(request, 'cooking/profile.html', context)
