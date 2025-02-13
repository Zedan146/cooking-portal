from django.shortcuts import render
from .models import Category, Post
from django.db.models import F  # Импортируем класс для подсчета просмотров постов


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
    context = {
        'title': articles.title,
        'post': articles,
    }
    return render(request, 'cooking/article_detail.html', context)
