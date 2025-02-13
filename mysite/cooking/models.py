from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Скоро появится...', verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото')
    watched = models.IntegerField(default=0, verbose_name='Колличество просмотров')
    is_published = models.BooleanField(default=True, verbose_name='Опубликованно?')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категории')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['id']
