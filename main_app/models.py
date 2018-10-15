from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
class Tool(models.Model):
    tool_name = models.CharField(max_length=75)
    tool_description = models.TextField(max_length=250)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # , initial='Tell us about yourself'
    bio = models.TextField(max_length=500)
    street1 = models.CharField(max_length=75)
    # initial='Street Address'
    street2 = models.CharField(max_length=75)
    # initial='e.g. Apt #'
    city = models.CharField(max_length=50)
    # initial='City'
    state = models.CharField(max_length=50)
    # initial='State'
    zipcode = models.IntegerField()
    # initial='Zip Code'

class Category(models.Model):
    tool_category = models.CharField(max_length=75)

class ToolRating(models.Model):
    date = models.DateField('Rating date')
    rating = models.CharField(
        max_length=1,
        # add the 'choices' field option
        choices=RATINGS,
        # set the default value for meal to be 'B'
        default=RATINGS[0][0]
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()