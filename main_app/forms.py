from django.forms import ModelForm, Form, CharField, IntegerField, PasswordInput, ModelMultipleChoiceField
from .models import Tool, Profile, Category, User, ToolRating

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'first_name', 'last_name', 'street1', 'street2', 'city', 'state', 'zipcode')

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ToolForm(ModelForm):
    # category = ModelMultipleChoiceField(queryset=Category.objects.all())
    # rating = ModelMultipleChoiceField(queryset=ToolRating.objects.all())
    class Meta:
        model = Tool
        fields = ('tool_name', 'tool_description')
    # def __init__(self, user, *args, **kwargs):
    #     super(ToolForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].queryset = Category.objects.all()
    #     self.fields['rating'].queryset = ToolRating.objects.all()

