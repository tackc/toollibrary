from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.urls import reverse

RATINGS = (
    ('1', 'Broken'),
    ('2', 'Poor'),
    ('3', 'Ok'),
    ('4', 'Good'),
    ('5', 'Excellent')
)

CATEGORIES = (
    ('1', '-'),
    ('2', 'Carpentry & Woodworking'),
    ('3', 'Electrical & Soldering'),
    ('4', 'Plumbing'),
    ('5', 'Lawn & Garden'),
    ('6', 'Miscellaneous')
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(max_length=500)
    street1 = models.CharField(max_length=75)
    street2 = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.user
    
    def get_absolute_url(self):
        return reverse('users_detail', kwargs={'user_id': user.id})

class Tool(models.Model):
    tool_name = models.CharField(max_length=75)
    tool_description = models.TextField(max_length=250)

class Category(models.Model):
    tool_category = models.CharField(max_length=75)

class ToolRating(models.Model):
    date = models.DateField('Rating date')
    rating = models.CharField(
        max_length=1,
        choices=RATINGS,
        default=RATINGS[0][0]
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()