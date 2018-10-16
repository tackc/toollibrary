from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('user/<username>/tools', views.tools_detail, name='tool_details')
    # path('tools/<int:tool_id>/add_photo/', views.add_photo, name='add_photo'),
]