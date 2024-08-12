from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Image(models.Model):
#  photo = models.ImageField(upload_to="usersprofileimage")

class Image(models.Model):
    photo = models.ImageField(upload_to="usersprofileimage", blank=True, null=True)  # Allow the photo field to be null and blank


    # oto = models.ImageField(upload_to="usersprofileimage", blank=True, null=True)  # Allow the photo field to be null and blank
    
class UserActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('image', 'Image Steganography'),
        ('audio', 'Audio Steganography'),
        ('video', 'Video Steganography'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=5, choices=ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"