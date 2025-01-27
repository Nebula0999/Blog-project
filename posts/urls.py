from django.urls import path
from .views import Index, About, Contact, ArticleDetail, LikeArticle, UnlikeArticle, Blog, ArticleDelete

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
    path('like/<int:pk>/', LikeArticle.as_view(), name='like-article'),
    path('article/<int:pk>/unlike/', UnlikeArticle.as_view(), name='unlike-article'),
    path('blog/', Blog.as_view(), name='blog'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article-delete'),
]