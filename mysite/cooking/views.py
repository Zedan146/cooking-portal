from django.shortcuts import render, redirect
from .models import Category, Post
from django.db.models import F  # Импортируем класс для подсчета просмотров постов
from .forms import PostAddForm, LoginForm, RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages


def index(request):
    """Отображение главной страницы"""
    posts = Post.objects.all()  # SELECT * FROM post
    context = {
        'title': 'Главаная страница',
        'posts': posts,
    }
    return render(request, 'cooking/index.html', context)


def category_list(request, pk):
    """Реакция на выбор категории"""
    posts = Post.objects.filter(category_id=pk)    # Отбираем посты по категории
    context = {
        'title': posts[0].category,
        'posts': posts,
    }
    return render(request, 'cooking/index.html', context)


def post_detail(request, pk):
    """Отображение страницы поста"""
    articles = Post.objects.get(pk=pk)  # Забираем нужный пост
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)  # Увеличиваем просмотр поста
    rec_post = Post.objects.all().exclude(pk=pk).order_by('-watched')[:4]
    context = {
        'title': articles.title,
        'post': articles,
        'rec_post': rec_post,
    }
    return render(request, 'cooking/article_detail.html', context)


def add_post(request):
    """Добавление статьи от пользователя, без динамики"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('post_detail', post.pk)
    else:
        form = PostAddForm()

    context = {
        'form': form,
        'title': 'Добавить статью'
    }
    return render(request, 'cooking/article_add_form.html', context)


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
