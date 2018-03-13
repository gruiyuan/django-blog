from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = 'Django 博客教程演示项目'
    # 通过聚合阅读器转到网址的地址
    link = "/"
    # 显示在聚合阅读器上的概述信息
    description = "Django博客教程演示项目测试文章"
    # 需要显示的内容条目
    def items(self):
        return Post.objects.filter(is_show=True)
    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)
    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body