from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.upload_files import upload_file_instance


class Message(models.Model):
    sender = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    message = models.TextField(_("Message text"), max_length=4096, blank=True, null=True)
    assets = models.FileField(_("assets"), upload_to=upload_file_instance, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} "

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
