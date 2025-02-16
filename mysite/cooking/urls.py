from django.urls import path
from .views import *
from .yasg import urlpatterns as api_doc_urls
from django.views.decorators.cache import cache_page

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    # path('', cache_page(60 * 15)(Index.as_view()), name='index'),
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
    path('password/', UserChangePassword.as_view(), name='change_password'),

    # API
    path('post/api/', CookingAPI.as_view(), name='cookingAPI'),
    path('post/api/<int:pk>', CookingAPIDetail.as_view(), name='cookingAPIDetail'),
    path('category/api/', CookingCategoryAPI.as_view(), name='cookingAPICategory'),
    path('category/api/<int:pk>', CookingCategoryAPIDetail.as_view(), name='cookingAPIDetailCategory'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += api_doc_urls
