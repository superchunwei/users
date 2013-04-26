# -*- coding: utf-8 -*-
__all__ = (
    'Point', 'Streak', 
)

from datetime import datetime

from django.db import models

import codepku.utils as utils

class Point(models.Model):
    """
    用户得分
    relation:
        point -> user: 1 - 1

    所有get 操作均不需要更新数据库
        inc 操作需要更新数据库

    所有的变化由 incScore 驱动

    Attention:
        only compare the date, not datetime
    """
    tem_score = models.IntegerField()
    # 上次记录时间
    his_date = models.DateField()
    # 历史最高分
    his_best_score = models.IntegerField() 
    total = models.IntegerField()
    class Meta:
        app_label = 'users'

    def inc(self, score, date=None):
        """
        args:
            score: score for this action
            date: today's date, only for test
        """
        today = datetime.today().date() \
                if date is None else date
        if self.his_date == today:
            self.tem_score += score
        else:
            # a new day
            self.his_date = today
            if self.tem_score > self.his_best_score:
                self.his_best_score = self.tem_score
            self.tem_score = score
        self.total += score
        self.save()

    def getToday(self, date=None):
        today = datetime.today().date() \
                if date is None else date
        if self.his_date == today:
            return self.tem_score
        else:
            # a new day
            return 0

    def getBest(self):
        if self.tem_score > self.his_best_score:
            return self.tem_score
        else:
            return self.his_best_score

    def getTotal(self):
        return self.total

    @property
    def today(self):
        return self.getToday()

    @property
    def best(self):
        return self.getBest()

    def __unicode__(self):
        return str((self.today, self.best, self.total))


class Streak(models.Model):
    """
    用户持续编程天数
    
    relation:
        user - steak: 1 to 1

    Attention:
        only compare date not datetime
    """
    # 上次记录时间
    last_date = models.DateField()
    tem_days = models.IntegerField()
    # best record
    best_days = models.IntegerField()
    total = models.IntegerField()
    
    class Meta:
        app_label = 'users'

    def inc(self, date=None):
        today = datetime.today().date() \
                if date is None else date

        if self.last_date == today:
            if self.tem_days == 0: 
                self.tem_days = 1
        # 连续
        elif utils.getDateInc(self.last_date, 1) == today:
            self.last_date = today
            self.tem_days += 1
        # another day
        else:
            if self.tem_days > self.best_days:
                self.best_days = self.tem_days
            self.tem_days = 1
            self.last_date = today
        self.save()

    def getStreak(self, date=None):
        today = datetime.today().date() \
                if date is None else date
        if self.last_date == today:
            return self.tem_days
        else:
            return 0

    def getBest(self):
        if self.tem_days > self.best_days:
            return self.tem_days
        return self.best_days

    @property 
    def streak(self):
        return self.getStreak()

    @property 
    def best(self):
        return self.getBest()

    def __unicode__(self):
        return str((self.streak, self.best))


