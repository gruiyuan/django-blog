from django import forms
from .models import Comment


#评论提交表单
class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['text']