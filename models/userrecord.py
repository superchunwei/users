# -*- coding: utf-8 -*-

from django.db import models
from codepku.lesson.models import Step
from codepku.users.models import User

class UserRecord(models.Model):
    """
    用户每一步的记录
    """
    input = models.TextField()
    addtime = models.DateTimeField()
    # relation
    user = models.ForeignKey(User)
    step = models.ForeignKey(Step)

    class Meta:
        app_label = 'users'

    def __unicode__(self):
        return self.input



