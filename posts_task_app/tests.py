# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from .models import Post


User = get_user_model()


USER_DATA = dict(
    username='username',
    email='username@gmail.com',
    password='password'
)


class CheckAuthorizationBase:
    """
    Checks auth

    """

    def setUp(self):
        self.client = Client()

    def test_response_code_401_or_302(self):
        response = self.client.get(self.url)

        # tests that response status code is 302 or 401
        self.assertIn(response.status_code, (302, 401))


class TestPostList(CheckAuthorizationBase, TestCase):
    """
    Tests get post list

    """

    url = reverse('posts_task_app:post-list')

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**USER_DATA)
        posts = []
        for _ in range(3):
            posts.append(
                Post(
                    title='title',
                    text='text',
                    user=self.user
                )
            )
        Post.objects.bulk_create(posts)

    def test_get_post_list(self):
        self.client.login(**USER_DATA)
        response = self.client.get(self.url)

        # tests that response status code is 200
        self.assertEquals(response.status_code, 200)

        # tests that response contains every post info
        for post in Post.objects.all():
            self.assertContains(response, post.title)


class TestPostDetail(CheckAuthorizationBase, TestCase):
    """
    Tests get post detail

    """

    post_data = dict(
        title='title',
        text='text'
    )

    def setUp(self):
        super().setUp()
        self.post_data['user'] = self.user = User.objects.create_user(
            **USER_DATA)
        self.post = Post.objects.create(**self.post_data)
        self.url = reverse('posts_task_app:post-detail', args=(self.post.id,))

    def test_get_post_detail(self):
        self.client.login(**USER_DATA)
        response = self.client.get(self.url)

        # tests that response status code is 200
        self.assertEquals(response.status_code, 200)

        # tests that response contains post info
        self.assertContains(response, self.post.title)


class TestPostCreate(CheckAuthorizationBase, TestCase):
    """
    Tests post creation, existing in the database, created by
    and invalid post creation

    """

    url = reverse('posts_task_app:post-create')

    valid_post_data = dict(
        title='title',
        text='text'
    )
    invalid_post_data = dict(
        title='title',
        text='text' * 2000
    )

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**USER_DATA)

    def test_post_create(self):
        self.client.login(**USER_DATA)
        response = self.client.post(self.url, self.valid_post_data)

        # tests that response status code is 200 or 302
        self.assertIn(response.status_code, (200, 302))

        # tests that created post exists in the database
        self.assertTrue(Post.objects.filter(
            title=self.valid_post_data['title']).exists())

        # tests that post was created by authenticated user
        self.assertEquals(Post.objects.last().user, self.user)

    def test_too_long_text(self):
        self.client.login(**USER_DATA)

        self.client.post(self.url, self.invalid_post_data)

        # tests that post with invalid data doesn't exist in the database
        self.assertFalse(Post.objects.exists())


class TestRegistration(TestCase):
    """
    Tests user registration, existing in the database
    and registration with invalid data

    """

    url = reverse('posts_task_app:register')

    valid_data = dict(
        username='example',
        email='example@gmail.com',
        password1='expass',
        password2='expass'
    )

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**USER_DATA)

    def test_user_created(self):
        response = self.client.post(self.url, self.valid_data)

        # tests that response status code is 200 or 302
        self.assertIn(response.status_code, (200, 302))

        # tests that user exists in the database
        self.assertTrue(User.objects.filter(
            username=self.valid_data['username']).exists())

    def test_username_already_exists(self):
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = self.user.username
        self.client.post(self.url, invalid_data)

        # tests that username is unique and only 1 user with this username
        # exists in the database, self.user
        self.assertTrue(User.objects.filter(
            username=invalid_data['username']).count() == 1)

    def test_invalid_username(self):
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = 'exa\mple<'
        self.client.post(self.url, invalid_data)

        # tests that user with invalid username doesn't exist in the database
        self.assertFalse(User.objects.filter(
            username=invalid_data['username']).exists())

    def test_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'example@\<.com'
        self.client.post(self.url, invalid_data)

        # tests that user with invalid email doesn't exist in the database
        self.assertFalse(User.objects.filter(
            username=invalid_data['username']).exists())

    def test_invalid_password(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password1'], invalid_data['password2'] = '', ''
        self.client.post(self.url, invalid_data)

        # tests that user with invalid password doesn't exist in the database
        self.assertFalse(User.objects.filter(
            username=invalid_data['username']).exists())

    def test_different_passwords(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password1'], invalid_data['password2'] = '12345', '12347'
        self.client.post(self.url, invalid_data)

        # tests that user that entered diff pass1 pass2 doesn't exist in the
        # database
        self.assertFalse(User.objects.filter(
            username=invalid_data['username']).exists())
