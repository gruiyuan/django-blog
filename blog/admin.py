from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Post, Category, Tag

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    exclude = ('author', 'views')
    #覆写save_model方法,将当前用户填入author字段
    def save_model(self, request, obj, form, change):
        if not obj.id:    #如果是创建过程
            obj.author = request.user
        obj.save()

admin.site.register(Category)
admin.site.register(Tag)
