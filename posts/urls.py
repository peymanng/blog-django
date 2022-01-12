from django.db import models

from django.urls import path ,re_path
from . import views
urlpatterns = [
    path("", views.posts, name="posts"),
    re_path(r"post/(?P<post>[-\w]+)", views.post, name="post"),
    re_path(r"(?P<tag_slug>[-\w]+)", views.posts, name="posts_tag"),
    re_path(r"like/(?P<post_slug>[-\w]+)",views.like, name="like")
]
