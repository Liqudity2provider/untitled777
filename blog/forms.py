from django import forms
from .models import Post, Categor


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post model
    """
    title = forms.CharField()
    category = forms.ModelChoiceField(required=False, queryset=Categor.objects.all())
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)
    content = forms.CharField(
        widget=forms.Textarea
    )

    class Meta:
        model = Post
        # fields = ['title', 'category', 'content', 'image', 'video']
        fields = ['title', 'content',]
