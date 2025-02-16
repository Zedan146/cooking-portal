from django import template
from cooking.models import Category
from django.db.models import Count, Q
from django.core.cache import cache


register = template.Library()


# @register.simple_tag()
# def get_all_categories():
#     """Кнопки категорий"""
#     # return Category.objects.all()
#     # return Category.objects.annotate(cnt=Count('post')).filter(cnt__gt=0)
#     return Category.objects.annotate(cnt=Count('post', filter=Q(post__is_published=True))).filter(cnt__gt=0)

@register.simple_tag()
def get_all_categories():
    """Кнопки категорий"""
    buttons = cache.get('category')

    if not buttons:
        Category.objects.annotate(cnt=Count('post', filter=Q(post__is_published=True))).filter(cnt__gt=0)
        cache.set('category', buttons, 60)

    return buttons
