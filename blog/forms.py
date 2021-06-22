from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post model
    """
    title = forms.CharField()
    category = forms.CharField(required=False)
    image = forms.FileField(required=False)
    video = forms.FileField(required=False)
    content = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image', 'video']
