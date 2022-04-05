from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User, models.CASCADE, verbose_name='Автор', related_name='post')
    post_name = models.CharField('Название поста', max_length=50)
    post_text = models.TextField('Текст поста')
    release_date = models.DateField('Дата публикации',  auto_now_add=True)

    def __str__(self):
        return (('Пост: \"%s\"') % (self.post_name))

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    author = models.ForeignKey(
        User, models.CASCADE, verbose_name='Автор', related_name='comment')
    post = models.ForeignKey(
        Post, models.CASCADE, related_name='comment')
    comment_text = models.TextField('Текст комментария')
    release_date = models.DateField('Дата публикации',  auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Profile(models.Model):
    user = models.OneToOneField(
        User, models.CASCADE, verbose_name='Профиль', related_name='profile')
    instagram_link = models.CharField('Инстаграм', max_length=50)
    facebook_link = models.CharField('Фейсбук', max_length=50)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Dialog(models.Model):
    send_date = models.DateTimeField(
        'Дата и время отправки',  auto_now_add=True)
    members = models.ManyToManyField(
        User, related_name='dialog', verbose_name='Учасники')
    flag = models.BooleanField('Группа', default=False)
    name = models.CharField('Название', default='Новая группа', max_length=50)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'


class Messages(models.Model):
    user = models.ForeignKey(
        User, models.CASCADE, verbose_name='Отправитель', related_name='outgoing_message')
    text = models.TextField('Текст')
    send_date = models.DateTimeField(
        'Дата и время отправки',  auto_now_add=True)
    read_status = models.BooleanField('Статус сообщения')
    dialog = models.ForeignKey(
        Dialog, models.CASCADE, related_name='message')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class InlinePost(admin.TabularInline):
    model = Post


class InlineComment(admin.TabularInline):
    model = Comment
