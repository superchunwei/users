# -*- coding: utf-8 -*-
from django.db import models

class Badge(models.Model):
    """
    用户勋章

    relation:
        user -> brand: one to many sorted by no
        brand -> step: one to one
    """
    no = models.IntegerField()
    name = models.CharField(max_length=30)
    # 图像链接
    url = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        app_label = 'users'

    def appendTo(self, user):
        user.badges.add(self)

    def __unicode__(self):
        return self.name
