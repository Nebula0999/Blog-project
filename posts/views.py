from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from posts.forms import ArticleForm, CommentForm
from posts.models import Article, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tinymce.models import HTMLField



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
    
class ArticleDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(article=article)
        return render(request, 'posts/article_detail.html', {'article': article, 'form': form, 'comments': comments})

    @method_decorator(login_required)
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            return redirect('article-detail', pk=pk)
        comments = Comment.objects.filter(article=article)
        return render(request, 'posts/article_detail.html', {'article': article, 'form': form, 'comments': comments})
    
    
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
    
@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.author != request.user:
            return redirect('index')
        form = ArticleForm(instance=article)
        return render(request, 'posts/article_update.html', {'form': form, 'article': article})

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.author != request.user:
            return redirect('index')
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article-detail', pk=article.pk)
        return render(request, 'posts/article_update.html', {'form': form, 'article': article})
    
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
    
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'posts/article_create.html', {'form': form})
    

    
    