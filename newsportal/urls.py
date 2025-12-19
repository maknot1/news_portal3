from django.urls import path
from .import views
from .views import (
    NewsList,
    NewsDetail,
    NewsCreate,
    NewsDelete,
    NewsUpdate,
    NewsSearch,
    ArticlesList,
)

urlpatterns = [

    # === NEWS ===
    path('', NewsList.as_view(), name='news_list'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('edit/<int:pk>/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),

    # === ARTICLES ===
    path('articles/', ArticlesList.as_view(), name='articles_list'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/', NewsDetail.as_view(), name='article_detail'),
    path('articles/<int:pk>/edit/', NewsUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='article_delete'),

    # === ПОДПИСКА ===#

    path('subscribe/<int:category_id>/', views.subscribe_to_category, name='subscribe_category'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe_category, name='unsubscribe_category'),


    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]