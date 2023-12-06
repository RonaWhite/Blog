"""定义blogs的URL模式"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blogs'

urlpatterns = [
    # 显示博客主页
    path('', views.index, name='index'),
    
    # 单个博客文章详细信息
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    
    # 创建博客页面
    path('create_blog/', views.create_blog, name='create_blog'),

    # 发布新博文页面
    path('publish_post/', views.publish_post, name='publish_post'),

    # 编辑现有博文页面
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)