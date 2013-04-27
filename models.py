# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib import admin 

import codepku.config as config

from submodels.meta import Point, Streak
from submodels.badge import Badge

class UserMeta(models.Model):
    """
    一些不常用到的,可能会被删除的用户信息
    """
    regist_ip = models.CharField(max_length=128, null=True, blank=True)
    regist_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    # TODO tinyint?
    status = models.IntegerField(null=True, blank=True)
    reset_key = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        app_label = 'users'


class User(models.Model):
    GENDER_CHOICES = (
            ("male", "男"),
            ("female", "女"),)
    name = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=64, null=True, blank=True)
    # TODO what is this?
    gender = models.CharField(max_length=4, 
            choices=GENDER_CHOICES, default='male')
    birth = models.DateTimeField(null=True, blank=True)
    work = models.CharField(max_length=64, null=True, blank=True)
    # userid of sina qq renren
    open_id = models.CharField(max_length=64, null=True, blank=True)
    open_token = models.CharField(max_length=128, null=True, blank=True)
    # sina qq renren
    # TODO change to integer
    open_type = models.CharField(max_length=64, null=True, blank=True)
    # meta
    point = models.OneToOneField(Point, null=True, blank=True)
    streak = models.OneToOneField(Streak, null=True, blank=True)
    badges = models.ManyToManyField(Badge)

    class Meta:
        app_label = 'users'

    def init(self):
        """
        init some data structure for user

        add 
            Point, Streak
        """
        today = datetime.today()
        # add a Point
        point = Point(
            tem_score = 0,
            his_date = today,
            his_best_score = 0,
            total = 0,
        )
        # add a Streak
        streak = Streak(
            last_date = today,
            tem_days = 0,
            # best record
            best_days = 0,
            total = 0,
        )
        point.save()
        streak.save()
        self.point = point
        self.streak = streak

        self.save()

    def addActivity(self, activity):
        """
        添加一个activity
        activity 的数量不能超过span
        """
        activities = self.activity_set.order_by('date').all()
        # automatically remove some activities more than config.activity
        if len(activities) == config.activity.span:
            # TODO is that action OK?
            del activities[-1]
        activity.save()

    def addTrack(self, course, chapter, step):
        """
        添加用户上课的轨迹
        一般在新的章节时执行
        如果已经有了同意Course, 则修改Chapter
        """
        try:
            track = Track.objects.get(course=course)
            if track.chapter != chapter:
                track.chapter = chapter
                track.step = step
        except:
            track = Track(course=course, user=self,
                        chapter=chapter, step=step)
        track.save()

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    """
    用户最近的动作

    relation:
        user -> activities: one to many
    """
    # date of activity
    date = models.DateTimeField()
    content = models.CharField(max_length=30)
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'users'

    def __unicode__(self):
        return str(self.user)


# --------------------- admins -----------------------------
class UserAdmin(admin.ModelAdmin):
    """
    list_display = ('name', 'email', 'password',
                    'gender', 'birth', 'work',
                    'reset_key', 'open_id', 'open_token',
                    'open_type',)
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'gender',
                    'password', 'birth', 'work',), 
            }),
        ('Advanced options', {
            'fields':( 'open_id', 'open_token',
            'open_type',),
        }),
    )
    search_fields = ('name',)

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', )

class PointAdmin(admin.ModelAdmin):
    list_display = ('tem_score', 'his_date', 'his_best_score', 'total', )

class StreakAdmin(admin.ModelAdmin):
    list_display = ('last_date', 'tem_days', 'best_days', 
                    'total',)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('date', 'content', 'user',)

admin.site.register(User, UserAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(Streak, StreakAdmin)
admin.site.register(Activity, ActivityAdmin)


