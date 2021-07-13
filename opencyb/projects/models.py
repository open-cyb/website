from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='projects')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    website = models.URLField(max_length = 200, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment: {} by {}'.format(self.body[:50]+'...', self.name)