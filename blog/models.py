# coding: utf-8

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

import markdown
from django.utils.html import strip_tags

#分类
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(u'分类名称', max_length=100)

    def __str__(self):
        return self.name

#标签
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(u'标签名称', max_length=100)

    def __str__(self):
        return self.name

#文章
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(u'标题', max_length=70) #文章标题
    body = models.TextField(u'正文') #文章正文
    created_time = models.DateTimeField(u'发表时间', auto_now_add=True) #发表时间
    modified_time = models.DateTimeField(u'更新时间', auto_now=True) #修改时间
    excerpt = models.CharField(u'摘要',max_length=200,blank=True) #文章摘要,允许留空
    #一篇文章只能属于一个分类，可以有多个标签
    category = models.ForeignKey(Category, verbose_name=u'分类')
    tags = models.ManyToManyField(Tag,blank=True, verbose_name=u'标签')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False) #作者
    is_show = models.BooleanField(u'展示', default=False)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']    #指定Post的默认排序方式
    #阅读量统计
    views = models.PositiveIntegerField(default=0)
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])    #只更新views字段从而提高效率
    #复写save方法，自动生成摘要
    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            #如果没有填写摘要，先将Markdown文本渲染成HTML文本
            #strip_tags去掉HTML文本的全部HTML标签
            #从文本摘取前54个字符赋值给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54] + ' ...'
        #调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)