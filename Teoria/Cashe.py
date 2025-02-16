import os.path
"""
Документация по кэшированию:
оригинал https://docs.djangoproject.com/en/5.1/topics/cache/,
русскоязычная https://django.fun/docs/django/5.0/topics/cache/
"""

# 1. Выставляем настройки кэширования в файле settings

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, 'web_site_cache'),   # Здесь мы указываем, где будет храниться наш кэш
    }
}

# -------------------------------------------------
# # -----Кэширование на базе файловой системы------
# -------------------------------------------------



# Указание кеша для каждого представления в URLconf

# Импортируем библиотеку
from django.views.decorators.cache import cache_page

# На примере Index закэшируем эту страницу, (60*15) - на 15 минут
# В точности так же можно закэшировать любую страницу
    path('', cache_page(60 * 15)(Index.as_view()), name='index'),


# ------------------------------------------
# # -----Кэширование на базе темплейтов-----
# ------------------------------------------

# Переходим на нужный нам шаблон, который будем кэшировать
# Загружаем кэш в шаблон {% load cache %}
# И закэшируем sidebar
"""
    <!-- Sidebar-->
        {% cache 500 sidebar %}    <------ Открываем кэш, на 500 секунд
                {% get_all_categories as categories %}
                {% for category in categories %}
                {% include 'cooking/inc/_category_buttom.html' %} 
                {% endfor %}    
        {% endcache %}    <------ Закрываем наш блок 
"""

# ----------------------------------------------
# # -----Кэширование на низкоуровневого API-----
# ----------------------------------------------

# cashe.set() - сохранение произвольных данных по ключу
# cashe.get() - выбор произвольных данных из кэша по ключу
# cashe.add() - заносит новое значение в кэш, если его там нет
# cache.get_or_set() - извлекает данные из кэша, если их нет, то автоматически заносит значение по умолчанию
# cache.delete() - удаление данных из кэша по ключу
# cache.clear() - полная очистка кэша

# @register.simple_tag()
# def get_all_categories():
#     """Кнопки категорий"""
#     buttons = cache.get('category')
#
#     if not buttons:
#         Category.objects.annotate(cnt=Count('post', filter=Q(post__is_published=True))).filter(cnt__gt=0)
#         cache.set('category', buttons, 60)
#
#     return buttons