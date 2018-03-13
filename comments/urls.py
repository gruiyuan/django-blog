from django.conf.urls import url

from . import views

#设定url命名空间
app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/(?P<user_pk>.+)/$', views.post_comment, name='post_comment'),    #评论post链接
]