from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.
class Gallery(models.Model):
  TAG_CHOICES = [
    ('people', 'People'),
    ('nature', 'Nature'),
    ('food', 'Food'),
    ('animal', 'Animal'),
    ('lifestyle', 'Lifestyle')
  ]
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length = 100)
  image = CloudinaryField('image')
  description = models.TextField()
  likes = models.ManyToManyField(User, related_name
     = 'liked_photo', blank = True )
  tag_category = models.CharField(max_length = 100, choices = TAG_CHOICES, default = 'people')
  
  def __str__(self):
    return self.user.username

