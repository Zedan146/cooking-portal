from django.contrib import admin
from .models import Category, Post, Comment  # Импротируем наши модели


# Класс для настройки админки модели постов
class PostAdmin(admin.ModelAdmin):
    # Отвечает за отображение нужных полей модели в админке
    list_display = ['id', 'title', 'category', 'watched', 'is_published', 'created_at', 'updated_at']
    # Отвечает за кликабельные поля в модели
    list_display_links = ['id', 'title']
    # Отвечает за изменение внутри модели, не заходя внутрь поста
    list_editable = ('is_published',)
    # Ставит поле только для чтения, нельзя менять через админку
    readonly_fields = ['watched']
    # Устанавливаем поля, по которым иожно фильтровать посты
    list_filter = ('is_published', 'category')


# Регистрируем наши модели в админке
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

