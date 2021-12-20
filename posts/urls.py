from django.db import models

from django.urls import path
from . import views
urlpatterns = [
    path("", views.posts, name="posts"),
    path("post/<str:post>", views.post, name="post"),
    path("<slug:tag_slug>", views.posts, name="posts_tag"),
    path("like/<slug:post_slug>",views.like, name="like")
]
