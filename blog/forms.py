from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post model
    """
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
