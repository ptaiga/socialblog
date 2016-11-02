from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()
    def __str__(self):
        return self.header