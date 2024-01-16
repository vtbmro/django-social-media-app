from django.forms import ModelForm
from django import forms
from .models import User, Post

class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ["text_content"]
        labels = {
            "text_content": ""
        }
        widgets = {
            "text_content": forms.Textarea(attrs={"rows":3})
        }