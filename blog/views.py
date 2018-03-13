import markdown
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q

from comments.form import CommentForm
from .models import Post, Category, Tag

#类视图,ListView的功能是从数据库中获取某个模型列表数据
class IndexView(ListView):
    model = Post    #指定要获取的模型
    template_name = 'blog/index.html'    #指定要渲染的模板
    context_object_name = 'post_list'    #指定获得的列表保存的变量名，将传递给模板
    #指定paginate_by属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10

    # 只显示is_show=True的文章
    def get_queryset(self):
        return super(IndexView, self).get_queryset().filter(is_show=True)

    def get_context_data(self, **kwargs):
        context =super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            #如果没有分页，则无需显示分页导航条
            return {}
        left = []    #当前页面左边连续的页码号
        right = []    #当前页面右边连续的页码号
        left_has_more = False    #标示第一页页码后面是否需要省略号
        right_has_more = False    #标示最后一页页面前面是否需要省略号
        first = False    #是否显示第一页页码：如果left列表不包含1，则需要显示
        last = False    #是否显示最后一页页码：如果right列表不包含最后一页页面，则需要显示

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]    #可以自定义右连续页码数
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]    #可以自定义左连续页码数
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if left[0] > 2:
                left_has_more = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages:
                last = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


class ArchivesView(IndexView):
    #覆写父类的get_queryset方法（默认获取指定模型的全部列表数据）
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')    #获取从url中捕获的值
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class Full_IndexView(IndexView):
    template_name = 'blog/full-index.html'



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    #覆写get方法，使得当文章被访问的同时调用该文章increase_views方法
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    #get_object方法:获取【数据表主键】=【从url中捕获的值】的对象
    #覆写get_object方法,渲染所获取的post的body
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)    #处理标题锚点值
            ])
        # 一旦调用了convert方法,md就会生成一个toc属性
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post
    #覆写get_context_data，除了将Post的数据传给模板外，额外传送其他内容
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()    #反向获取该文章下的所有评论
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

'''
#搜索功能视图
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    #'i'代表不区分大小写;Q对象用于包装查询表达式，其提供复杂的查询逻辑（例如下面的'|'）
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #阅读量+1
    post.increase_views()
    #渲染Markdown
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      #拓展功能，详见官方文档http://pythonhosted.org/Markdown/extensions/index.html
                                      'markdown.extensions.extra',    #额外拓展
                                      'markdown.extensions.codehilite',    #语法高亮拓展
                                      'markdown.extensions.toc',    #允许自动生成目录
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()    #反向获取该文章下的所有评论
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

def full_index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/full-index.html', context={'post_list': post_list})

#归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,    #作为函数参数列表，Django要求把表示属性的'.'换成'__'
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})

#分类视图
def category(request, pk):
    #post_list = Post.objects.filter(category_id=pk)
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
'''
