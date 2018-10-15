from django.forms import ModelForm, Form, CharField, IntegerField, PasswordInput
from .models import Tool, Profile, Category

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'street1', 'street2', 'city', 'state', 'zipcode')

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'