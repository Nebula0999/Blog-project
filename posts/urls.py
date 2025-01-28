from django.urls import path
from .views import Index, About, Contact, ArticleDetailView, LikeArticle, UnlikeArticle, Blog, ArticleDelete, create_article, ArticleUpdateView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('like/<int:pk>/', LikeArticle.as_view(), name='like-article'),
    path('article/<int:pk>/unlike/', UnlikeArticle.as_view(), name='unlike-article'),
    path('blog/', Blog.as_view(), name='blog'),
    path('create/', create_article, name='create-article'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article-delete'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article-update'),
]