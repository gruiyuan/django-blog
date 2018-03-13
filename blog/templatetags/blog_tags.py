from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category, Tag

register = template.Library() #实例化一个template.Library类

#最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.filter(is_show=True)[:num]

#归档模板标签
@register.simple_tag
def archives():
    return Post.objects.filter(is_show=True).dates('created_time', 'month')

#分类模板标签
@register.simple_tag
#统计每个分类的文章数
def get_categories():
    return Category.objects.filter(post__is_show=True).annotate(num_posts=Count('post')).filter(num_posts__gt=0)    #文章数>0的分类才给予显示

#标签云
@register.simple_tag
def get_tags():
    return Tag.objects.filter(post__is_show=True).annotate(num_posts=Count('post')).filter(num_posts__gt=0)