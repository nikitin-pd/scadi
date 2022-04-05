from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('post<int:post_id>/', views.post, name='post'),
    path('user<int:user_id>/', views.user, name='user'),
    path('reg_page/', views.reg_page, name='reg_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('comment_delete<int:comment_id>/',
         views.comment_delete, name='comment_delete'),
    path('comment_edit<int:comment_id>/',
         views.comment_edit, name='comment_edit'),
    path('user<int:user_id>/create_post/',
         views.create_post, name='create_post'),
    path('myprofile',
         views.myprofile, name='myprofile'),
    path('editmyprofile',
         views.editmyprofile, name='editmyprofile'),
    path('user<int:user_id>/send_message/',
         views.send_message, name='send_message'),
    path('my_messages/',
         views.my_messages, name='my_messages'),
    path('my_messages/dialog<int:dialog_id>/',
         views.dialog, name='dialog'),
    path('my_messages/new_group/',
         views.new_group, name='new_group'),
    path('my_messages/dialog<int:dialog_id>/edit/',
         views.group_edit, name='group_edit'),
    path('my_messages/dialog<int:dialog_id>/del<int:member_id>/',
         views.group_edit_del, name='group_edit_del'),
    path('my_messages/dialog<int:dialog_id>/add<int:member_id>/',
         views.group_edit_add, name='group_edit_add'),
]
