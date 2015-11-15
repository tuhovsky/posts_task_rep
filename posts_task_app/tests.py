# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Post


class TestAuthorizationBaseClass(TestCase):

    url = reverse('posts_task_app:post-list')

    def setUp(self):
        self.client = Client()

    def test_response_code_401_or_302(self):
        response = self.client.get(self.url)

        # tests that response status code is 401 or 302
        self.assertIn(response.status_code, (401, 302))


class TestPostList(TestAuthorizationBaseClass):

    url = reverse('posts_task_app:post-list')
    user_data = dict(
        username='user',
        password='password'
    )

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**self.user_data)
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
        self.client.login(**self.user_data)
        response = self.client.get(self.url)

        # tests that response status code 200
        self.assertEquals(response.status_code, 200)

        # tests that response has every post info
        for post in Post.objects.all():
            self.assertContains(response, post.title)


class TestPostDetail(TestAuthorizationBaseClass):

    user_data = dict(
        username='user',
        password='password'
    )
    post_data = dict(
        title='title',
        text='text'
    )

    def setUp(self):
        super().setUp()
        self.post_data['user'] = self.user = User.objects.create_user(
            **self.user_data)
        self.post = Post.objects.create(**self.post_data)

    def test_get_post_detail(self):
        self.client.login(**self.user_data)
        response = self.client.get(reverse('posts_task_app:post-detail',
                                           args=(self.post.id,)))

        # tests that response status code 200
        self.assertEquals(response.status_code, 200)

        # tests that response has post info
        self.assertContains(response, self.post.title)


class TestPostCreate(TestAuthorizationBaseClass):

    url = reverse('posts_task_app:post-create')
    user_data = dict(
        username='user',
        password='password'
    )
    valid_post_data = dict(
        title='title',
        text='text'
    )

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**self.user_data)

    def test_post_create(self):
        self.client.login(**self.user_data)
        valid_post_data = dict(
            title='title',
            text='text'
        )
        response = self.client.post(
            self.url, valid_post_data
        )
        # tests that response status code is 200 or 302
        self.assertIn(response.status_code, (200, 302))

        # tests that created post exist in the database
        self.assertTrue(Post.objects.filter(
            title=valid_post_data['title']).exists())

        # tests that post was created by authenticated user
        self.assertEquals(Post.objects.last().user, self.user)

    def test_too_long_text(self):
        self.client.login(**self.user_data)
        invalid_post_data = dict(
            title='title',
            text='text' * 2000
        )
        self.client.post(self.url, invalid_post_data)
        self.assertFalse(Post.objects.exists())
