from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.urls import reverse

RATINGS = (
    (1, '-'),
    (2, 'Broken'),
    (3, 'Poor'),
    (4, 'Ok'),
    (5, 'Good'),
    (6, 'Excellent')
)

CATEGORIES = (
    (1, '-'),
    (2, 'Carpentry & Woodworking'),
    (3, 'Electrical & Soldering'),
    (4, 'Plumbing'),
    (5, 'Lawn & Garden'),
    (6, 'Miscellaneous')
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    bio = models.TextField(max_length=500, null=True)
    street1 = models.CharField(max_length=75, null=True)
    street2 = models.CharField(max_length=75, blank=True, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.user.username + "'s Profile"
    
    def get_absolute_url(self):
        return reverse('users_detail', kwargs={'user_id': user.id})

class Tool(models.Model):
    tool_name = models.CharField(max_length=75)
    tool_description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool_name

    # def get_absolute_url(self):
    #     return reverse('tools_detail', kwargs={'tool_id': tool.id})

class Category(models.Model):
    tool_category = models.IntegerField(
        choices=CATEGORIES,
        default=CATEGORIES[0][0]
    )
    tools = models.ManyToManyField(Tool)

    def __str__(self):
        return str(CATEGORIES[self.tool_category][1])

    def get_absolute_url(self):
        return reverse('tool_list')

class ToolRating(models.Model):
    rating = models.IntegerField(
        choices=RATINGS,
        default=RATINGS[0][0]
    )
    tools = models.ManyToManyField(Tool)

    def __str__(self):
        return str(RATINGS[self.rating][1])

    def get_absolute_url(self):
        return reverse('tool_list')

class ToolPhoto(models.Model):
    url = models.CharField(max_length=200)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for tool_id: {self.tool_id} @{self.url}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()