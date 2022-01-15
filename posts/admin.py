from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers
from .models import Category, Post , Comment  , IP

# ** ---------------------Actions--------------------
@admin.action(description='export selected posts as json')
def export_as_json(modeladmin , request , queryset):
    response = HttpResponse(content_type = 'application/json')
    serializers.serialize('json',queryset,stream=response)
    return response


@admin.action(description='Make all ratings 5')
def rate_to_five(modeladmin, request, queryset):
    result = queryset.update(rate=5)

    modeladmin.message_user(request , f'{result} posts were rated to 5')


@admin.action(description="inactive selected comments")
def inactive_comments(modeladmin , request , queryset):
    result = queryset.update(active=False)
    modeladmin.message_user(request , f'{result} posts were inactivated')

# ** -----------------register------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title' , 'get_categories', 'slug' , 'get_visits' , 'number_of_likes' , 'tag_list' , 'pub_date')
    prepopulated_fields = {'slug' : ('title' ,)}
    actions=[rate_to_five , export_as_json]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    list_editable = ('active',)
    actions = [inactive_comments]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title' , 'slug')
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(IP)