from django.shortcuts import render, redirect
from .forms import LoginForm, ProfileForm, ToolForm
from .models import Tool, Profile, Category, ToolRating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector'

# Create your views here.

def index(request):
    return render(request, 'index.html')

# TOOLS PAGES
# def add_tool(request):
#     tools = Tool.objects.all()
#     return render(request, 'tools/index.html', {'tools': tools})
@login_required
def tools_index(request):
    tools = Tool.objects.all()
    return render(request, 'tools/index.html', {'tools': tools})

def tools_detail(request, tool_id):
    tool = Tool.objects.get(id=tool_id)
    return render(request, 'tools/detail.html', {
    	'tool': tool
    })

# def tools_detail(request):
#     tool = Tool.objects.get(tool=tool)
#     update_url = f"/tool/{tool.id}/update"
#     return render(request, 'tools/detail.html', {'tool': tool, 'update_url': update_url})

def tools_create(request):
    if request.method == 'POST':
        # updated_data = request.POST.copy()
        # category = int(updated_data.get('category'))
        # rating = int(updated_data.get('rating'))
        # del updated_data['category']
        # del updated_data['rating']
        # updated_data['category'] = category
        # updated_data['rating'] = rating
        # print("this is the updated data:")
        # print(updated_data)

        form = ToolForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return HttpResponseRedirect('/tools/')
        else:
            print("we got errors:")
            print(form.errors)
    else:
        form = ToolForm()
        return render(request, 'main_app/tool_form.html', {'form': form})

# class ToolCreate(CreateView):
#     model = Tool
#     # fields = ['tool_name', 'tool_description', 'category', 'rating']
#     # fields = '__all__'
#     # categories = Category.objects.all()
#     # ratings = ToolRating.objects.all()
#     form_class = ToolForm
    
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         return HttpResponseRedirect('/tools/')

class ToolUpdate(UpdateView):
    model = Tool
    fields = ['tool_name', 'tool_description']
    
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.tool = self.request.tool
    #     self.object.save()
    #     return HttpResponseRedirect(f'/{self.request.tool.tool_id}/tool')
        # return render(request, 'main_app/tool_form.html', {'form': form})

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
    tools = Tool.objects.filter(user=user)
    update_url = f"/users/{user.id}/profile/update"
    return render(request, 'profile.html', {'username': username, 'profile': profile, 'update_url': update_url, 'tools': tools})

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'bio', 'street1', 'street2', 'city', 'state', 'zipcode']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(f'/{self.request.user.username}/profile')