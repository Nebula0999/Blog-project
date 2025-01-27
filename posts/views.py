from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.models import Article



class Index(ListView):
    model = Article
    template_name = 'posts/index.html'
    context_object_name = 'articles'
    queryset = Article.objects.all().order_by('-date_posted')
    paginate_by = 5

class Blog(ListView):
    model = Article
    template_name = 'posts/blog.html'
    context_object_name = 'articles'
    queryset = Article.objects.all().filter(featured=True).order_by('-date_posted')
    paginate_by = 5


class About(View):
    def get(self, request):
        return render(request, 'posts/about.html')
    
class Contact(View):
    def get(self, request):
        return render(request, 'posts/contacts.html')
    
class ArticleDetail(DetailView): 
    model = Article
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        return render(request, 'posts/article_detail.html', {'article': article})
    
    def get_context_data(self, **kwargs):
        context =  super(ArticleDetail, self).get_context_data(**kwargs)
        context['liked_by_user'] = False
        article = Article.objects.get(pk=self.kwargs['pk'])
        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user'] = True
        return context

    
    
class LikeArticle(View):
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user)
        article.save()
        return render(request, 'posts/article_detail.html', {'article': article})
    
class UnlikeArticle(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user.id)
        return redirect('article-detail', pk=pk)
    
class ArticleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    template_name = 'posts/article_confirm_delete.html'
    
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'posts/article_confirm_delete.html', {'article': article})
    
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk) 
        article.delete()
        return redirect('index')
    
    def test_func(self):
        article = self.get_object()
        return self.request.user.id == article.author.id
 