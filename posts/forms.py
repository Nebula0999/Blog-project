from django import forms
from .models import Article, Comment
#from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ArticleForm(forms.ModelForm):
    content = HTMLField()


    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category', 'featured']