from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()
ADMIN_NUMBER_OF_CHARACTERS = 15


class Group(models.Model):
    title = models.CharField(
        help_text='Название сообщества не должно быть длиннее 200 символов',
        max_length=200,
        verbose_name='Название группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес группы'
    )
    description = models.TextField(
        help_text='Добавьте описание сообщества.',
        verbose_name='Описание группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        help_text='Текст не должен быть длиннее 700 символов',
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа, к которой будет относиться пост',
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:ADMIN_NUMBER_OF_CHARACTERS]
