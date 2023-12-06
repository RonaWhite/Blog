from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse

from .models import Blog, Post
from .forms import BlogForm, PostForm

def index(request):
    """博客的主页"""
    blogs = Blog.objects.all()  # 获取所有博客对象
    post_id = request.GET.get('post_id')  # 从请求中获取 post_id 参数
    context = {'blogs': blogs, 'post_id': post_id}  # 将 post_id 加入上下文
    return render(request, 'blogs/index.html', context)

def blog_detail(request, blog_id):
    """单个博客文章详细信息"""
    blog = Blog.objects.get(pk=blog_id)  # 获取特定 ID 的博客文章
    return render(request, 'blogs/blog_detail.html', {'blog': blog})


def create_blog(request):
    """创建博客页面"""
    if request.method != 'POST':
        form = BlogForm()  # 创建一个新博客表单
    else:
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return redirect('blogs:index')  # 假设重定向到博客主页

    context = {'form': form}
    return render(request, 'blogs/create_blog.html', context)


@login_required
def publish_post(request):
    """发布新博文页面"""
    if request.method != 'POST':
        form = PostForm()  # 创建一个新博文表单
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user

            try:
                blog = Blog.objects.get(author=request.user)
            except Blog.DoesNotExist:
                # 如果用户没有博客对象，为其创建一个新的博客对象
                blog = Blog.objects.create(author=request.user, title="My Blog")
            
            new_post.blog = blog  # 将新博文与当前用户的博客关联

            new_post.save()
            return redirect('blogs:index')  # 假设重定向到博客主页

    context = {'form': form}
    return render(request, 'blogs/publish_post.html', context)



@login_required
def edit_post(request, post_id):
    """编辑现有博文页面"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    if post.author != request.user:
        # 处理未授权的情况，比如重定向到错误页面或返回错误消息
        return HttpResponse("You are not authorized to edit this post.")

    
    if request.method != 'POST':
        form = PostForm(instance=post)  # 初次请求，使用当前博文填充表单
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')  # 假设重定向到博客主页

    context = {'form': form, 'post_id': post_id}
    return render(request, 'blogs/edit_post.html', context)