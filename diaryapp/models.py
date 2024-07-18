from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DairyEntry(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")