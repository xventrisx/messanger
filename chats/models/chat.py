import uuid

from django.db import models


class Chat(models.Model):
    _CHAT_TYPE = (
        ("D", "dialog"),
        ("G", "group"),
        ("CH", "channel"),
    )
    name = models.CharField(default=uuid.uuid4, editable=True, unique=True)
    chat_type = models.CharField(max_length=1, choices=_CHAT_TYPE)
    date_created = models.DateTimeField(auto_now_add=True)
