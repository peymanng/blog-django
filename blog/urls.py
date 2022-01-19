from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import create_post
from .views import index , contact_us_view , search

urlpatterns = [
    path('admin/', admin.site.urls),
    # *Third-Party urls
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    # *My apps urls
    path('posts/', include('posts.urls')),
    path('create-post/' , create_post , name='create-post'),
    path('' , index , name='home'),
    path('contact-us' , contact_us_view , name='contact-us'),
    path('search' , search , name='search'),
]
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)