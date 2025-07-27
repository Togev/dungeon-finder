from django.conf import settings
from django.db import models


from table_groups.models import Table


# Create your models here.
class TableMessage(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)