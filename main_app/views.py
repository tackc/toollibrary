from django.shortcuts import render, redirect
from .forms import LoginForm, ProfileForm
from .models import Tool, Profile, Category, ToolRating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'index.html')

# TOOLS PAGES
# def add_tool(request):
#     tools = Tool.objects.all()
#     return render(request, 'tools/index.html', {'tools': tools})

def tools_index(request):
    tools = Tool.objects.all()
    return render(request, 'tools/index.html', {'tools': tools})

def tools_detail(request, tool_id):
    tool = Tool.objects.get(id=tool_id)
    return render(request, 'tools/detail.html', {
    	'tool': tool
    })

class ToolCreate(CreateView):
    model = Tool
    fields = '__all__'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/tools/')

class ToolUpdate(UpdateView):
    model = Tool
    fields = ['name', 'description', 'category', 'rating']

@method_decorator(login_required, name='dispatch')
class ToolDelete(DeleteView):
    model = Tool
    success_url = '/tools'

def add_photo(request, tool_id):
	# photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, tool_id=tool_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('tools_detail', tool_id=tool_id)

# Login, logout, signup, profile views
def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(f'/users/{user.id}/profile/update')
        else:
            print("this is the form...")
            print(form)
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    update_url = f"/users/{user.id}/profile/update"
    return render(request, 'profile.html', {'username': username, 'profile': profile, 'update_url': update_url})

# Update profile
# @login_required
# def update_profile(request, username):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save()
#             return HttpResponseRedirect(f"/{username}/profile")
#         else:
#             print("form was invalid somehow")
#             print(form.errors)
#     else:
#         user = User.objects.get(username=request.user.username)
#         profile = Profile.objects.get(user=user)
#         # profile = user.profile
#         # print("this is the user profile:")
#         # print(profile.bio)
#         # print(profile.street1)
#         form = ProfileForm(instance=profile)
#         return render(request, 'profile.html', {'username': username, 'profile': profile, 'form': form})

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'bio', 'street1', 'street2', 'city', 'state', 'zipcode']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(f'/{self.request.user.username}/profile')