from django.db import models

from django.urls import path ,re_path
from . import views
urlpatterns = [
    path("", views.posts, name="posts"),
    path("categories/", views.categories, name="categories"),
    re_path(r"category/(?P<category_slug>[-\w]+)", views.category, name="category"),
    re_path(r"like/(?P<post_slug>[-\w]+)",views.like, name="like"),
    re_path(r"post/(?P<post>[-\w]+)", views.post, name="post"),
    re_path(r"(?P<tag_slug>[-\w]+)", views.posts, name="posts_tag"),
]
