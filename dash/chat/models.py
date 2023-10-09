import uuid

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from dash.helpers.admin_panel import customTitledFilter
from dash.helpers.file import RandomFileName


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatSession(TrackableDateModel):
    """ A Chat Session. """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User, related_name="members")

    def get_last_message(self):
        msg = ChatSessionMessage.objects.filter(
            chat_session_id=self.id).order_by("-created").first()
        if msg:
            if msg.image:
                return "📁 Photo"
            else:
                return msg.message
        return None

    class Meta:
        ordering = ('-updated',)
        verbose_name_plural = "Chat Sessions"


class ChatSessionMessage(TrackableDateModel):
    """Store messages for a session."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=RandomFileName(
        'chats'), null=True, blank=True)
    is_read = models.BooleanField(default=False)

    # def to_json(self):
    #     """deserialize message to JSON."""
    #     return {'user': deserialize_user(self.user), 'id': self.id, 'message': self.message, 'is_read': self.is_read, 'time': self.created_at}

    class Meta:
        verbose_name_plural = "Chat Session Messages"


@admin.register(ChatSession, site=admin.site)
class ChatSessionTable(admin.ModelAdmin):
    model = ChatSession
    list_per_page = settings.TABLE_PAGINATION_CST
    search_fields = ("id",)
    list_filter = (
        ("created", customTitledFilter("Created Date")),
    )
    list_display = [f.name for f in model._meta.fields]


@admin.register(ChatSessionMessage, site=admin.site)
class ChatSessionMessageTable(admin.ModelAdmin):
    model = ChatSessionMessage
    list_per_page = settings.TABLE_PAGINATION_CST
    search_fields = ("id", "user__username")
    list_filter = (
        ("created", customTitledFilter("Created Date")),
    )
    list_display = [f.name for f in model._meta.fields]
