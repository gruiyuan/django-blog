from django.conf.urls import url, include
from django.contrib import admin
from blog.feed import AllPostsRssFeed

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'users/', include('django.contrib.auth.urls')),
    url(r'', include('blog.urls')),
    url(r'', include('comments.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
]