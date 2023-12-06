"""定义blogs的URL模式"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blogs'

urlpatterns = [
    # 显示博客主页
    path('', views.index, name='index'),
    
    # 显示所有博客文章的页面
    path('blogs/', views.blogs, name='blogs'),
    
    # 特定博客文章的详细页面
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    
    # 添加博客主题的页面
    path('add_blog/', views.add_blog, name='add_blog'),

    # 发布新博文的页面
    path('publish_post/<int:blog_id>/', views.publish_post, name='publish_post'),

    # 编辑现有博文页面
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)