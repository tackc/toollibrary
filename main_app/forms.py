from django.forms import ModelForm, Form, CharField, IntegerField, PasswordInput
from .models import Tool, Profile, Category, User

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'first_name', 'last_name', 'street1', 'street2', 'city', 'state', 'zipcode')

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

# class ToolForm(ModelForm):
#     class Meta:
#             model = Tool
#             fields = ('name', 'description')