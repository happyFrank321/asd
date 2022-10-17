from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group


User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        help_text="Текст поста(расскажите что-нибудь интересное)"
        )
    
    pub_date = models.DateTimeField(
        "date published", 
        auto_now_add=True
        )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="posts"
        )
    
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        help_text='Группа(необязательное поле)'
        )

    class Meta:
        ordering=['-pub_date']
        
    def __str__(self):
        return self.text

