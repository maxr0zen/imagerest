from django.db import models
from django.contrib.auth.models import User
import os


def image_rename(instance, filename):
    new_filename = f"post_{instance.id}_{filename}"
    current_path = instance.image.path

    new_path = os.path.join(os.path.dirname(current_path), new_filename)
    os.rename(current_path, new_path)
    return f"post_images/{new_filename}"


class Post(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=False)
    created_at = models.DateField(auto_now_add=True)

    def count_likes(self):
        return self.like_set.count()


class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    created_at = models.DateField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


