from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    image = models.ImageField(default='default.jpg', upload_to='images/')

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
