from .models import Comment 
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ( 'body' ,)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control comment-form'