from django.db import models
from django.db.models.base import Model

# Create your models here.
class Average(models.Model):
    author = models.TextField()
    averages = models.TextField()
    last_update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.author
    
    