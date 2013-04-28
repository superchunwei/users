# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models

today = datetime.today().date() 
#.strftime("%Y-%m-%d"),

class Point(object):
    def __init__(self, tem_score=0, his_date=today,
            his_best_score=0, total=0, *args, **kwargs):

        self.tem_score = tem_score 
        # 上次记录时间
        try:
            self.his_date = his_date.date()
        except:
            self.his_date = his_date
        # 历史最高分
        self.his_best_score = his_best_score
        self.total = total

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

    def getToday(self, date=None):
        today = datetime.today().date() \
                if date is None else date
        print '@@his_date % today:', self.his_date, today
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
        return str(
            (self.today, self.best, self.total))

    def __repr__(self):
        return '<Point: %s>' % str(
            (self.today, self.best, self.total))


class PointField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(PointField, self).__init__(*args, **kwargs)  

    def to_python(self, value):
        """
        将数据库中的值转化为python 对象
        """
        if isinstance(value, Point):
            return value
        if value == '' or value is None:
            return Point()
        from dateutil import parser as dateparser
        value = value.strip()
        # remove ()
        value = value[1:value.rfind(')')]
        values = value.split(',')
        tem_score, his_date, his_best_score, total = \
        int(values[0]), dateparser.parse(value[1]), \
        int(values[2]), int(values[3])
        return Point(tem_score, his_date, his_best_score, total)

    def get_db_prep_value(self, value, *args, **kwargs):
        return str(
            (value.tem_score, value.his_date.strftime("%Y-%m-%d"), 
            value.his_best_score, value.total))

    def db_type(self, connection):  
        return 'point_type'



