from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.contrib import messages

from .models import Blog, Post
from .forms import BlogForm, PostForm

def index(request):
    """博客的主页"""
    return render(request, 'blogs/index.html')

@login_required
def blogs(request):
    """显示所有的博客"""
    blogs = Blog.objects.filter(owner=request.user).order_by('date_added')
    context = {'blogs': blogs}
    return render(request, 'blogs/blogs.html', context)

@login_required
def blog(request, blog_id):
    """显示单个博客及其所有的文章"""
    blog = Blog.objects.get(id=blog_id)
    # 确认请求的博客属于当前用户
    if blog.author != request.user:
        raise Http404
    
    posts = blog.post_set.order_by('-date_added')
    context = {'blog': blog, 'posts': posts}
    return render(request, 'blogs/blog.html', context)

@login_required
def add_blog(request):
    """添加博客主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = BlogForm()
    else:
        # POST提交的数据：对数据进行处理
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.author = request.user  # 确保为 author 字段赋值为当前用户
            new_blog.save()
            return redirect('blogs:blogs')

    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'blogs/add_blog.html', context)

@login_required
def publish_post(request, blog_id):
    """发布新博文"""
    blog = Blog.objects.get(id=blog_id)
    
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.blog = blog
            new_post.author = request.user  # 设置博文的作者为当前登录用户
            new_post.save()
            return redirect('blogs:blog', blog_id=blog_id)
    else:
        form = PostForm()
    
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/publish_post.html', context)


    # 显示空表单或指出表单数据无效
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/publish_post.html', context)

@login_required
def edit_post(request, post_id):
    """编辑既有的文章"""
    post = Post.objects.get(id=post_id)
    blog = post.blog
    if blog.author != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 初次请求：使用当前的文章填充表单
        form = PostForm(instance=post)
    else:
        # POST提交的数据：对数据进行处理
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)

    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_post.html', context)
