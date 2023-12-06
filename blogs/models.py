from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    """博客模型"""
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)  # 创建时间
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_blogs')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_blogs')

    description = models.TextField(blank=True)  # 描述，可以为空
    cover_image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)  # 封面图，允许为空

    def __str__(self):
        return self.title  # 返回博客标题作为字符串表示

class Post(models.Model):
    """博文模型"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 博文作者关联到用户模型
    date_added = models.DateTimeField(auto_now_add=True)  # 创建时间
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)  # 外键关联到博客模型

    tags = models.CharField(max_length=100, blank=True)  # 标签，可以为空，可以根据需要更改数据类型
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # 图片，允许为空
    likes = models.IntegerField(default=0)  # 点赞数，默认为0

    def __str__(self):
        return self.title  # 返回博文标题作为字符串表示
