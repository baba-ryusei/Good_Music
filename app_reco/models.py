from django.db import models
import uuid

#グループモデル
class Group(models.Model):
    name = models.CharField(max_length=100)
    group_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.name

# 曲モデル
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    url = models.URLField(default="http://example.com")
    group = models.ForeignKey(Group, related_name='songs', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)  # いいねの数を保持するフィールド


    def __str__(self):
        return f'{self.title} by {self.artist}'
