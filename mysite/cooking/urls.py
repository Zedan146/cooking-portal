from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<int:pk>/', ArticleByCategory.as_view(), name='category_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/add_article/', AddPost.as_view(), name='add_post'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_registrations, name='user_registration'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchResult.as_view(), name='search'),
    path('add_comment/<int:post_id>', add_comment, name='add_comment'),
    path('profile/<int:user_id>', profile, name='profile'),
]


