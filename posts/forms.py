from .models import Comment 
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CommentForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = Comment
        fields = ( 'body' ,)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control comment-form'