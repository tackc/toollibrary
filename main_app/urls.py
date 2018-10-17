from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('<username>/profile', views.profile, name='profile'),
    # TOOLS PAGES
    path('tools/', views.tools_index, name='tools_index'),
    path('tools/<int:tool_id>', views.tools_detail, name='tools_detail'),
    path('tools/create/', views.ToolCreate.as_view(), name='tools_create'),
    path('tools/<int:pk>/update/', views.ToolUpdate.as_view(), name='tools_update'),
    path('tools/<int:pk>/delete/', views.ToolDelete.as_view(), name='tools_delete'),
    path('tools/<int:tool_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('tools/<int:tool_id>/add_photo/', views.add_photo, name='add_photo'),
    # path('user/<username>/tools', views.tools_detail, name='tool_details'),
]