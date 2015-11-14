from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .models import User, Post
from .views import PostList


class TestAuthorizationBaseClass(TestCase):

    url = reverse('posts_task_app:post-list')

    def setUp(self):
        self.client = Client()

    def test_response_code_401_or_302(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)


class TestPostList(TestAuthorizationBaseClass):

    url = reverse('posts_task_app:post-list')

    def setUp(self):
        self.user = User.objects.create(username='user_1',
                                        email='user_1@gmail.com',
                                        password='111111',)
        self.user.posts.create(title='post_1_title', text='post_1_text')
        self.user.posts.create(title='post_2_title', text='post_2_text')
        self.user.posts.create(title='post_3_title', text='post_3_text')

    def test_get_post_list(self):

        self.client.login(username='user_1', password='111111')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(response.context['object_list']), 3)

# Create your tests here.
