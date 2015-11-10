from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 3


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'text', 'create_at', )
    search_fields = ['title', 'text']
    list_per_page = 10


class UserAdmin(UserAdmin):
    fieldsets = [
        ('User', {
         'fields': ['username', 'email', 'password']
         }),
    ]
    list_display = ('username', 'email', 'last_login')
    search_fields = ['username', 'email', ]
    list_per_page = 10
    inlines = [PostInline]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
