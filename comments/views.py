from django.shortcuts import render, get_object_or_404, redirect
from users.models import User
from blog.models import Post

from .models import Comment
from .form import CommentForm

def post_comment(request, post_pk, user_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        #检验数据是否合法
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)   #commit=False表示仅保存模型实例，但不存入数据库
            comment.user = user    #评论与用户关联
            comment.post = post    #将评论与被评论文章关联起来
            comment.save()    #将评论存进数据库
            #重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL
            return  redirect(post)
        else:
            #如果数据不合法，再重定向到详情页的同时，保留填写的内容，并渲染表单的错误
            comment_list = post.comment_set.all()    #反向查询关联文章的所有评论,等价于'Comment.object.filter(post=post)'
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    #不是post请求，重定向到文章详情页
    return redirect(post)
