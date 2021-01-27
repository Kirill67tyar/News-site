from django.contrib.auth import views as autho_views
from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'news'

urlpatterns = [
    # path('', views.index, name='home'), # http://127.0.0.1:8000/first/index/
    # path('', cache_page(60)(views.HomeNews.as_view()), name='home'),    # в as_vew() мы можем передавать параметры
# устанавливаем кэш главной страницы на одну минуту
    path('', views.HomeNews.as_view(), name='home'), # сравни время загрузки с кэшированием и без

    # path('category/<int:pk>/', views.get_category, name='category'),
    path('category/<int:pk>/', views.NewsByCategory.as_view(), name='category'),

    # path('news/<int:news_id>', views.view_news, name='view_news'),
    path('news/<int:pk>', views.ViewNews.as_view(), name='view_news'),

    # path('news/add-news/', views.add_news, name='add_news'),
    path('news/add-news/', views.CreateNews.as_view(), name='add_news'),

    path('console/', views.console, name='console'),

    path('test-pagination/', views.test_pagination, name='pagination'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('contact/', views.sender_email, name='contact'),


]


# urlpatterns = [
#     path('index/', views.index1, name='home'), # http://127.0.0.1:8000/first/index/
#     path('console/', views.console, name='console'),
#     path('index/category/<int:pk>/', views.index1, name='category'),
#
#
# ]