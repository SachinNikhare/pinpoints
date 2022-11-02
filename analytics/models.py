from itertools import count
from django.db import models
from shortener.models import pinpointsURL

# Create your models here.
class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance,pinpointsURL):
            obj, created = self.get_or_create(pinpoints_url=instance)
            obj.count   += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    pinpoints_url   = models.OneToOneField(pinpointsURL, on_delete=models.CASCADE)
    count           = models.IntegerField(default=0)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    objects         = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
