from http import HTTPStatus

from posts.models import Post, Group
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


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
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()

    def test_create_post(self):
        """Валидная форма создает пост в Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст, создаваемого поста',
            'group': self.group,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Валидная форма создает пост в Post."""
        source_post = Post.objects.create(
            text='Исходный текст поста',
            author=self.user,
            group=self.group
        )
        self.another_group = Group.objects.create(
            title='Название второй группы',
            slug='another-group-slug',
            description='Описание второй группы'
        )
        form_data = {
            'text': 'Изменённый текст',
            'group': self.another_group.id
        }
        response = self.guest_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotEqual(source_post.text, form_data['text'])
        self.assertNotEqual(source_post.group, form_data['group'])
