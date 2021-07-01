from django import forms
from .models import Comment
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('parent', 'content')

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


class CommentAdminDeleteForm(forms.Form):
    reason_for_deleting = forms.CharField(label='Reason for deleting', max_length=100)
