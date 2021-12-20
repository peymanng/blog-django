from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from .views import index , contact_us_view , search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('posts/', include('posts.urls')),
    path('' , index , name='home'),
    path('contact-us' , contact_us_view , name='contact-us'),
    path('search' , search , name='search'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)