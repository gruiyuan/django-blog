from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'blog' #视图函数的命名空间
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),    #首页（as_view方法将类视图转化为函数视图）
    url(r'^full-index/$', views.Full_IndexView.as_view(), name='full_index'),    #宽屏
    url(r'^about/$', TemplateView.as_view(template_name='blog/about.html'), name='about'),    #关于
    url(r'^contact/$',TemplateView.as_view(template_name='blog/contact.html'), name='contact'),    #联系
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),    #文章页面
    url(r'^archives/(?P<year>[1-9]\d{3})/(?P<month>[1-9]|1[0-2])/$', views.ArchivesView.as_view(), name='archives'),    #归档页面
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),    #分类页面
    url(r'tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),    #标签页面
]