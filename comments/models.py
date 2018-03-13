from django.conf import settings
from django.db import models
from django.utils.six import python_2_unicode_compatible

#评论
@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)    #用户名
    text = models.TextField()   #评论内容
    created_time = models.DateTimeField(auto_now_add=True)  #评论时间，自动指定为评论生成时间
    #文章可以有多个评论
    post = models.ForeignKey('blog.Post')

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return  self.text[:20]
