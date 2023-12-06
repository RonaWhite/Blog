from django import forms
from .models import Blog, Post

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'cover_image']
        labels = {'title': 'Title', 'description': 'Description', 'cover_image': 'Cover Image'}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'image']
        labels = {'title': 'Title', 'content': 'Content', 'tags': 'Tags', 'image': 'Image'}
        widgets = {'content': forms.Textarea(attrs={'rows': 10, 'cols': 80})}  # 自定义 content 字段的文本区域大小
