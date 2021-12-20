from django.shortcuts import get_list_or_404, render
from posts.models import Post
from django.db.models import Q

def index(request):
    latest_posts = Post.objects.all().order_by('-pub_date')[:3]

    return render(request , 'posts/home.html' , {'posts' : latest_posts })

def search(request):
    data = request.POST
    posts = Post.objects.filter(Q(title__icontains=data['search']) | Q(body__icontains=data['search']) | Q(tags__name__icontains=data['search']) ).distinct()
    search = None
    if posts:
        search = True 
    context = {'posts' : posts , 'search' : search , 'searched': data['search'] }
    return render(request , 'posts/posts.html' , context)

def contact_us_view(request):
    return render(request , 'contact-us.html')