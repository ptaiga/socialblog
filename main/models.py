from django.db import models

class Article(models.Model):
    header = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    content = models.TextField()