from django.db import models

class Post(models.Model):
    STATUS_CHOICES = [('draft','Draft'), ('published','Published'), ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# Create your models here.
