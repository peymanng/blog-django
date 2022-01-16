from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField 
User = get_user_model()

class IP(models.Model):
    ip = models.GenericIPAddressField()
    
    def __str__(self):
        return self.ip



class Category(models.Model):
    title = models.CharField(max_length=100 , unique=True)
    slug = models.SlugField()
    description = models.CharField(max_length=130 , null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True , allow_unicode=True)
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name='post')
    description = models.CharField(max_length=100)
    rate = GenericRelation(Rating)
    body = RichTextUploadingField()
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like' , blank=True)
    image = models.ImageField(upload_to='posts/')
    tags = TaggableManager()
    visits = models.ManyToManyField(IP , blank=True , related_name='visits')

    def __str__(self):
        return self.title
    
    def get_categories(self):
        return ' , '.join([category.title for category in self.category.all()])

    def get_absolute_url(self):
        return f'/posts/post/{self.slug}'

    def get_visits(self):
        return self.visits.count()

    def number_of_likes(self):
        return self.likes.count()
    
class Comment(models.Model): 
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) 
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies' , on_delete=models.SET_NULL)

    class Meta: 
        ordering = ('-created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post) 
    
    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    