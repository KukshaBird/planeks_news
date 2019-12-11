from django import forms
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'editable'})

    class Meta:
        model = Post
        fields = ['title', 'text', ]

class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'editable'})

    class Meta:
        model = Comment
        fields = ['text', ]

