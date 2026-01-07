from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def get_content_snippet(self):
        return self.content[0:5] + "..."


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
