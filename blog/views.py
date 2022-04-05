from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Post, Comment, Profile, Messages, Dialog
from .forms import PostForm, CommentForm, UserLogForm, UserRegForm, UserProfileForm, MoreUserProfileForm, MessageForm, GroupForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login
from pywebio.input import *
from pywebio.output import *


def group_edit_del(request, dialog_id, member_id):
    group = Dialog.objects.get(id=dialog_id)
    members = group.members.exclude(id=member_id)
    new_members = []
    for i in members:
        new_members.append(i)
    group.members.clear()
    for i in new_members:
        group.members.add(i)
    memebers_in = group.members.all()
    users = User.objects.all()
    group.save()
    return render(request, 'blog/group_edit.html', {'group': group, 'memebers_in': memebers_in, 'users': users, })


def group_edit_add(request, dialog_id, member_id):
    group = Dialog.objects.get(id=dialog_id)
    new_member = User.objects.get(id=member_id)
    group.members.add(new_member)
    memebers_in = group.members.all()
    users = User.objects.all()
    group.save()
    return render(request, 'blog/group_edit.html', {'group': group, 'memebers_in': memebers_in, 'users': users, })


def group_edit(request, dialog_id):
    group = Dialog.objects.get(id=dialog_id)
    memebers_in = group.members.all()
    users = User.objects.all()
    return render(request, 'blog/group_edit.html', {'group': group, 'memebers_in': memebers_in, 'users': users, })


def new_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            new_group = Dialog.objects.create(flag=True)
            new_group.name = group.name
            for i in group.members.all():
                new_group.members.add(i)
            new_group.members.add(request.user)
            new_group.save()
            return redirect(('/my_messages/dialog%s') % (str(new_group.id)), pk=new_group.id)
    else:
        form = GroupForm()
        return render(request, 'blog/new_group.html', {'form': form, })


def message(request, message_id):
    message = Messages.objects.get(id=message_id)
    message.read_status = True
    message.save()
    if request.user.is_authenticated:
        return render(request, 'blog/message.html', {'message': message})


def dialog(request, dialog_id):
    dialog = Dialog.objects.get(id=dialog_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.read_status = False
            message.dialog = Dialog.objects.get(pk=dialog_id)
            message.save()
            return redirect(('/my_messages/dialog%s') % (str(dialog_id)), pk=dialog_id)
    else:
        form = MessageForm()
        return render(request, 'blog/dialog.html', {'form': form, 'user': request.user, 'dialog': dialog})


def my_messages(request):
    if request.user.is_authenticated:
        user = request.user
        dialogs = Dialog.objects.filter(members=request.user)
        return render(request, 'blog/my_messages.html', {'user': user, 'dialogs': dialogs})


def send_message(request, user_id):
    user = User.objects.get(id=request.user.id)
    recipient = User.objects.get(id=user_id)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = user
            message.read_status = False
            if Dialog.objects.filter(members__id=user.id, flag=False).filter(members__id=recipient.id, flag=False):
                dialog = Dialog.objects.filter(members__id=user.id, flag=False).filter(
                    members__id=recipient.id, flag=False)[0]
                message.dialog = dialog
                message.save()
                return redirect(('/my_messages/dialog%s') % (str(dialog.id)), pk=dialog.id)
            else:
                new_dialog = Dialog.objects.create()
                new_dialog.members.set([user, recipient])
                new_dialog.flag = False
                new_dialog.save()
                message.dialog = new_dialog
                message.save()
                return redirect(('/my_messages/dialog%s') % (str(new_dialog.id)), pk=new_dialog.id)
    else:
        form = MessageForm()
        return render(request, 'blog/send_message.html', {'form': form, 'recipient': recipient})


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = post.comment.all()
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = User.objects.get(pk=user_id)
                comment.post = post
                comment.save()
                return redirect(('/post%s/') % (str(post.id)), pk=post.pk)
        else:
            form = CommentForm()
            return render(request, 'blog/post.html', {'form': form, 'post_name': post.post_name, 'post_text': post.post_text, 'author': post.author, 'release_date': post.release_date, 'comments': comments, 'user': request.user, 'post': post})
    else:
        return render(request, 'blog/npost.html', {
            'post_name': post.post_name,
            'post_text': post.post_text,
            'author': post.author,
            'release_date': post.release_date,
        })


def myprofile(request):
    if request.user.is_authenticated:
        return render(request, 'blog/myprofile.html', {'user': request.user})


def editmyprofile(request):
    user = request.user
    if request.method == "POST":
        form1 = UserProfileForm(request.POST, instance=user)
        if form1.is_valid():
            new_data = form1.save()
            new_data.save()
            form2 = MoreUserProfileForm(request.POST, instance=user)
            if form2.is_valid():
                user.profile.instagram_link = form2.cleaned_data['instagram_link']
                user.profile.facebook_link = form2.cleaned_data['facebook_link']
                user.profile.save()
                return redirect('/myprofile', pk=user.id)
    else:
        form1 = UserProfileForm(instance=user)
        form2 = MoreUserProfileForm(instance=user.profile)
        return render(request, 'blog/editmyprofile.html', {'form1': form1, 'form2': form2, 'user': user})


def user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.user.is_authenticated:
        if user_id == request.user.id:
            return render(request, 'blog/profile.html', {
                'posts': user.post.all(),
                'user': user,
                'flag': False,
            })
        else:
            return render(request, 'blog/user.html', {
                'posts': user.post.all(),
                'user': user,
                'flag': True,
            })
    else:
        return render(request, 'blog/user.html', {
            'posts': user.post.all(),
            'user': user,
            'flag': False,
        })


def create_post(request, user_id):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(pk=user_id)
            post.save()
            return redirect(('/post%s/') % (str(post.pk)), pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def login_page(request):
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(('/'), pk=user.pk)
            else:
                return render(request, 'blog/error_login_page.html', {'form': form})
        else:
            print(form.errors)
    else:
        form = UserLogForm()
        return render(request, 'blog/login_page.html', {'form': form})


def reg_page(request):
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],)
            Profile.objects.create(user=user)
            return redirect(('/login_page'), pk=user.pk)
    else:
        form = UserRegForm()
    return render(request, 'blog/reg_page.html', {'form': form})


def main(request):
    users = User.objects.filter(is_staff=False, is_active=True)
    posts = Post.objects.all()
    if request.user.is_authenticated:
        return render(request, 'blog/main.html', {
            'user': request.user,
            'users': users,
            'posts': posts,
        })
    else:
        return render(request, 'blog/nmain.html', {
            'users': users,
            'posts': posts,
        })


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'blog/logout_page.html')


def comment_delete(request, comment_id):
    comment = request.user.comment.get(id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect(('/post%s') % (str(post_id)), pk=post_id)


def comment_edit(request, comment_id):
    comment = request.user.comment.get(id=comment_id)
    post_id = comment.post.id
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            new_comment = form.save()
            new_comment.save()
            return redirect(('/post%s') % (str(post_id)), pk=post_id)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'blog/comment_edit.html', {'form': form, })
