from django.shortcuts import get_object_or_404, redirect, render , get_list_or_404
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .models import Category, Post , Comment
from .forms import CommentForm
from .forms import CreatePostForm
# from django.views.decorators.http import require_safe
# Create your views here.



def posts(request , tag_slug=None):
        posts = Post.objects.all().order_by('-pub_date')
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = Post.objects.filter(tags__name__in=[tag])
        paginator = Paginator(posts, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {'posts' : page_obj , 'tag' : tag}

        return render(request , 'posts/posts.html' , context)


def categories(request):
    categories = Category.objects.all()
    return render(request , 'posts/categories.html' , {'categories' : categories})


def category(request , category_slug):
    posts = get_list_or_404(Post,category__title__icontains=category_slug)
    return render(request , 'posts/posts.html' , {'posts' : posts})


def post(request , post):
    post = get_object_or_404(Post , slug=post)
    comments = post.comments.filter(active=True)
    if request.user.ip_address not in post.visits.all():
        post.visits.add(request.user.ip_address)

    visits = post.visits.count()
    new_comment = None
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent_obj = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user.username
            new_comment.email = request.user.email
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {'post' : post,
               'comments': comments,
               "visits": visits ,
               'new_comment': new_comment,
               'comment_form': comment_form ,
               'post_is_liked' : liked,
               'number_of_likes' : post.number_of_likes(),
               }

    return render(request , 'posts/post.html' , context)

def like(request , post_slug):
    post = get_object_or_404(Post , slug=post_slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post' , post=post_slug)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST , request.FILES)
        if form.is_valid():
            print(form.cleaned_data['tags'])
            slug = slugify(form.cleaned_data['title'] , allow_unicode=True)
            category = form.cleaned_data['category'][0]
            image = request.FILES['image']
            post = Post.objects.create(
                title =form.cleaned_data['title'],
                slug = slug,
                author = request.user,
                description = form.cleaned_data['description'],
                body = form.cleaned_data['body'],
                image = image,
            )
            for i in form.cleaned_data['tags']:
                post.tags.add(i)
            post.category.add(category)
            post.save()
            return redirect('home')
        else:
            return render(request, "posts/create_post.html", {'form':form}) 
        
    form = CreatePostForm()        
    return render(request , 'posts/create_post.html' , {'form' : form})