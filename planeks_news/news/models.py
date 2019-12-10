from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    in_premoderetion = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', blank=True)

    class Meta:
        permissions = [
            ("can_moderate", "Can change text, approve and decline posts."),
        ]

    def publish(self):
        self.in_premoderetion = False
        self.is_published = True
        self.published_date = timezone.now()
        self.save()

    def decline(self):
        self.in_premoderetion = False
        self.is_declined = False
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_post_comments', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = [
            ("can_moderate", "Can change text."),
        ]

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
