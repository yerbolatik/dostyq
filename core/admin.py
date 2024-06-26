from django.contrib import admin

from core.models import Post, Gallery, Friend, FriendRequest, Comment, ReplyComment, Notification, Group, GroupPost, Page, PagePost, ChatMessage, GroupChat, GroupChatMessage, GroupPostComment, ReplyGroupPostComment


class GalleryAdminTab(admin.TabularInline):
    model = Gallery


class CommentTabAdmin(admin.TabularInline):
    model = Comment


class GroupPostCommentTabAdmin(admin.TabularInline):
    model = Comment


class ReplyCommentTabAdmin(admin.TabularInline):
    model = ReplyComment


class GroupPostTabAdmin(admin.TabularInline):
    model = GroupPost


class PostAdmin(admin.ModelAdmin):
    inlines = [GalleryAdminTab, CommentTabAdmin]
    list_editable = ['active']
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    prepopulated_fields = {"slug": ('title',)}


class GroupPostAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['thumbnail', 'user', 'title', 'visibility', 'active']
    prepopulated_fields = {"slug": ('title',)}


class GalleryAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['thumbnail', 'post', 'active']


class FriendRequestAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['sender', 'receiver', 'status']


class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend']


class CommentAdmin(admin.ModelAdmin):
    # inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'post', 'comment', 'active']


class GroupPostCommentAdmin(admin.ModelAdmin):
    # inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'post', 'comment', 'active']


class ReplyAdmin(admin.ModelAdmin):
    # inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'comment', 'reply', 'active']


class ReplyGroupPostAdmin(admin.ModelAdmin):
    # inlines = [ReplyCommentTabAdmin]
    list_display = ['user', 'comment', 'reply', 'active']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type',
                    'sender', 'post', 'comment', 'is_read']


class GroupAdmin(admin.ModelAdmin):
    list_editable = ['name', 'visibility']
    list_display = ['thumbnail', 'user', 'name', 'visibility']
    prepopulated_fields = {"slug": ('name',)}


class PageAdmin(admin.ModelAdmin):
    list_editable = ['user', 'name', 'visibility']
    list_display = ['thumbnail', 'user', 'name', 'visibility']
    prepopulated_fields = {"slug": ('name',)}


class ChatMessageAdmin(admin.ModelAdmin):
    list_editable = ['message']
    list_display = ['sender', 'receiver', 'message', 'is_read']


class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'host', 'active']
    prepopulated_fields = {"slug": ("name", )}


class GroupChatMessageAdmin(admin.ModelAdmin):
    list_display = ['groupchat', 'sender', 'message', 'is_read', 'date']


admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GroupPostComment, GroupPostCommentAdmin)
admin.site.register(ReplyComment, ReplyAdmin)
admin.site.register(ReplyGroupPostComment, ReplyGroupPostAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GroupPost, GroupPostAdmin)
admin.site.register(PagePost)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(GroupChatMessage, GroupChatMessageAdmin)
admin.site.register(GroupChat, GroupChatAdmin)
