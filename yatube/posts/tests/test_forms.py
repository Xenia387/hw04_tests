from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


URL_POST_DETAIL = 'posts:post_detail'
URL_POST_CREATE = 'posts:post_create'
URL_POST_EDIT = 'posts:post_edit'


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Описание тестовой группы',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает пост в Post."""
        posts_count = Post.objects.count()
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group.id}
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        request_post = Post.objects.first()
        self.assertEqual(request_post.text, form_data['text'])
        self.assertEqual(request_post.group.id, form_data['group'])
        self.assertNotEqual(posts_count, posts_count + 1)

    def test_edit_post(self):
        """Валидная форма изменяет пост в Post."""
        source_post = Post.objects.create(
            text='Исходный текст поста',
            author=self.user,
            group=self.group,
        )
        another_group = Group.objects.create(
            title='Название второй группы',
            slug='another-group-slug',
            description='Описание второй группы'
        )
        form_data = {
            'text': 'Изменённый текст',
            'group': another_group,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': source_post.id}),
            data=form_data,
            follow=True,
        )
        source_post.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(source_post.text, form_data['text'])
        self.assertNotEqual(source_post.group, form_data['group'])
