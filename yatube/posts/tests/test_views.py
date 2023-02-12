from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group
from posts.utils import POSTS_NUMBER

User = get_user_model()
LIST_OF_TEST_POSTS = 13


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'):
                'posts/index.html',
            reverse('posts:profile', kwargs={'username': self.post.author}):
                'posts/profile.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/post_create.html',
            reverse('posts:post_create'):
                'posts/post_create.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        """Шаблон index сорфмирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, self.user.username)
        self.assertEqual(post_group_0, self.group.title)

    def test_grouplist_correct_context(self):
        """Шаблон group_list сорфмирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, self.user.username)
        self.assertEqual(post_group_0, self.group.title)

    def test_profile_correct_context(self):
        """Шаблон profile сорфмирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.post.author})
        )
        first_object = response.context['page_obj'][0]
        post_text_0 = first_object.text
        post_author_o = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_o, self.user.username)
        self.assertEqual(post_group_0, self.group.title)

    def test_postdetail_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        post_text_0 = {
            response.context.get('post').text: 'Текст поста',
            response.context.get('post').group: 'Тестовая группа',
        }
        for value, expected in post_text_0.items():
            self.assertEqual(post_text_0[value], expected)

    def test_editpost_correct_context(self):
        """Шаблон edit_post сорфмирован с правильным контекстом"""
        response = (self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_postcreate_correct_context(self):
        """Шаблон post_create сорфмирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_created_post_added_correctly(self):
        """Пост при создании добавлен корректно"""
        post = Post.objects.create(
            text='Созданный пост',
            author=self.user,
            group=self.group
        )
        response_index = self.authorized_client.get(
            reverse('posts:index')
        )
        response_group = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        index = response_index.context['page_obj']
        group = response_group.context['page_obj']
        profile = response_profile.context['page_obj']
        self.assertIn(post, index, 'поста нет на главной')
        self.assertIn(post, group, 'поста нет в профиле')
        self.assertIn(post, profile, 'поста нет в группе')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый пост',
        )
        cls.empty_list = []
        for i in range((LIST_OF_TEST_POSTS - 1)):
            cls.empty_list.append(
                Post(
                    author=cls.user,
                    group=cls.group,
                    text=f'Текст тестового поста номер {i}'
                )
            )
        Post.objects.bulk_create(cls.empty_list)

    def test_first_page_contains_ten_posts(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:profile', kwargs={'username': self.post.author}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        ]
        for i in pages:
            response = self.client.get(i)
            self.assertEqual(len(response.context['page_obj']), POSTS_NUMBER)

    def test_second_page_contains_three_posts(self):
        pages = [
            reverse('posts:index'),
            reverse('posts:profile', kwargs={'username': self.post.author}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
        ]
        for i in pages:
            response = self.client.get(i + '?page=2')
            self.assertEqual(
                len(response.context['page_obj']),
                (LIST_OF_TEST_POSTS - POSTS_NUMBER)
            )
