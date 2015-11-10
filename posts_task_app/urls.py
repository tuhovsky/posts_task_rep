from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [

    url(r'^accounts/login/$',
        login,
        name='login'),

    url(r'^accounts/logout/$',
        logout,
        name='logout'),

    url(r'^accounts/register/$',
        views.register,
        name='register'),

    url(r'^posts-list/$',
        views.posts_list,
        name='posts-list'),

    url(r'^(?P<post_id>[0-9]+)/$',
        views.post_detail,
        name='post-detail'),

    url(r'^post-create/$',
        views.post_create,
        name='post-create'),

]
