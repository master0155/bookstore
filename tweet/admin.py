from django.contrib import admin
from tweet.models import Tweet, Like, Comment


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'tweet', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'tweet', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at']
