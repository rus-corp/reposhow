from django.contrib import admin

from app.chat.models import ChatRoom, Messages, Thread, Comment


admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(ChatRoom)
admin.site.register(Messages)
