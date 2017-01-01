from django import forms
from .models import Post

from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'author',
            'image',
            'draft',
            'publish',
        ]