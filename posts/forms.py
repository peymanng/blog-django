from dataclasses import fields
from pyexpat import model
import string
from .models import Comment, Post 
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title' , 'category' , 'description' , 'body' , 'image' , 'tags')

class CommentForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = Comment
        fields = ( 'body' ,)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control comment-form'