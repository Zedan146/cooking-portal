from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', category_list, name='category_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/add_article/', add_post, name='add_post'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_registrations, name='user_registration'),
]
