from django.conf import settings
from django.db import models

try:
    from django.utils.timezone import now
except:
    import datetime
    now = datetime.datetime.now


class DelegatedView(models.Model):
    url = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    created = models.DateTimeField(default=now)
    finished = models.DateTimeField(blank=True, null=True)

    pickled_request = models.TextField()
    status_code = models.CharField(max_length=10, blank=True)
    content_type = models.CharField(max_length=64, blank=True)

    data_size = models.PositiveIntegerField(default=0)
    data = models.FileField(upload_to='delegated_views/', blank=True, null=True)
