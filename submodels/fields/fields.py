# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
import codepku.utils as utils

today = datetime.today().date() 

class Streak(object):
    def __init__(self, tem_score=0, last_date=today.strftime("%Y-%m-%d"), 
                 tem_days=0, best_days=0, total=0, *args, **kwargs):
        # 临时记录
        self.tem_score = tem_score
        # 上次记录时间
        self.last_date = last_date
        self.tem_days = tem_days
        # best record
        self.best_days = best_days
        self.total = total

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
    
    def __repr__(self):
        return '<Streak: %>' % str((self.streak, self.best))

class StreakField(models.Field):
    """
    用户持续编程天数
    
    relation:
        user - steak: 1 to 1

    Attention:
        only compare date not datetime
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(StreakField, self).__init__(*args, **kwargs)  

    def db_type(self, connection):  
        return 'streak_type'

    def to_python(self, value):
        """
        将数据库中的值转化为python 对象
        """
        if isinstance(value, StreakField):
            return value
        from dateutil import parser as dateparser
        value = value.strip()
        # remove ()
        value = value[1:value.rfind(')')]
        print value
        values = value.split(',')
        tem_score, last_date, tem_days, best_days, total= \
        int(values[0]), dateparser.parse(value[1]), \
        int(values[2]), int(values[3]), int(value[4])
        return StreakField(tem_score, last_date, tem_days, best_days, total)

    def get_db_prep_value(self, value, *args, **kwargs):
        return str(
            (self.tem_days, self.last_date,
             self.tem_days, self.best_days, self.total))



