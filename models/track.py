# -*- coding: utf-8 -*-

from django.db import models
from codepku.users.models import User 
from codepku.lesson.models import  Chapter, Step

class Track(models.Model):
    """
    用户学习过的课程

    tracks: [ {   course_name: name ,
                chapter_name: name, 
                step: no, 
                step_len: length of steps
            } ],
    """
    user = models.ForeignKey(User)
    chapter = models.ForeignKey(Chapter)
    step = models.ForeignKey(Step)

    class Meta:
        app_label = 'users'

    def flush(self):
        """
        如果chapter 已经存在, 更新step
        """
        try:
            track = self.user.track_set.get(chapter=self.chapter)
            # update certain
            track.step = self.step
            track.save()
        except Exception, e:
            # TODO save error in log ?
            self.save()

    @property
    def course_name(self):
        return self.chapter.course.name

    @property
    def chapter_name(self):
        return self.chapter.name

    @property
    def step_no(self):
        return self.step.no

    @property
    def step_len(self):
        return len(self.chapter.step_set.all())

    def __unicode__(self):
        return str((self.course_name, self.chapter_name, 
                    self.step_no, self.step_len))
