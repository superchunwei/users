# -*- coding: utf-8 -*-

__all__ = (
    'UserTest', 'PointTest', 'StreakTest',
    'TrackTest',
)

from datetime import datetime, timedelta

from django.test import TestCase
from codepku.users.models import *
from codepku.lesson.models import *
from codepku.record.models import *
from codepku.users.submodels.fields import PointField, StreakField

def initDB():
    course = Course(
        name='js',
    )
    course.save()
    
    chapter1 = Chapter(
        no = 1,
        name='chapter-1',
        course = course
    )
    chapter1.save()
    
    step1_1 = Step(
        title = 'step1_1',
        no = 1,
        chapter = chapter1
    )
    step1_1.save()

    step1_2 = Step(
        title = 'step1_2',
        no = 2,
        chapter = chapter1
    )
    step1_2.save()

    chapter2 = Chapter(
        no = 2,
        name='chapter-2',
        course = course
    )
    chapter2.save()

    step2_1 = Step(
        title = 'step2_1',
        no = 1,
        chapter = chapter2
    )
    step2_1.save()

    step2_2 = Step(
        title = 'step2_2',
        no = 2,
        chapter = chapter2
    )
    step2_2.save()


class UserTest(TestCase):

    def setUp(self):
        self.user = User(name='superjom')
        self.user.save()
        initDB()

    def test_init(self):
        #self.user.init()
        print '.. user s point:'
        print self.user.point
        print '.. user s steak:'
        print self.user.streak

    def test_add_activity(self):
        today = datetime.today()
        activity = Activity(
            date = today,
            content = 'activity 1',
            user = self.user,
        )
        self.user.addActivity(activity)
        print '.. all activity:'
        print Activity.objects.all()
        print '.. user s activity:'
        print self.user.activity_set.all()

    def test_addTrack(self):
        pass


class PointTest(TestCase):
    """
    对pointfield 进行测试
    """
    def setUp(self):
        self.user = User(name='superjom')
        #self.user.init()
        self.user.save()

    def test_python(self):
        print 'point', self.user.point


    def test_inc(self):
        point = self.user.point
        print '###### point is ', point
        today = datetime.today().date() 
        tomorrow = today + timedelta(days=1)
        point.inc(1)
        self.assertEqual(
                (point.today, point.best, point.total),
                (1, 1, 1)
        )
        point.inc(2)
        self.assertEqual(
                (point.today, point.best, point.total),
                (3, 3, 3)
        )
        point.inc(2, tomorrow)
        self.assertEqual(
                (point.getToday(tomorrow), point.best, point.total),
                (2, 3, 5)
        )
        point.inc(5, tomorrow)
        self.assertEqual(
                (point.getToday(tomorrow), point.best, point.total),
                (7, 7, 10)
        )




class StreakTest(TestCase):
    def setUp(self):
        self.user = User(name='superjom')
        #self.user.init()
        self.user.save()

    def test_inc(self):
        streak = self.user.streak
        today = datetime.today().date() 
        tomorrow = today + timedelta(days=1)
        tomorrow_1 = today + timedelta(days=2)
        tomorrow_3 = today + timedelta(days=4)

        streak.inc(today)
        self.assertEqual(
                (streak.getStreak(today), streak.best),
                (1, 1)
        )
        streak.inc(tomorrow)
        self.assertEqual(
                (streak.getStreak(tomorrow), streak.best),
                (2, 2)
        )
        streak.inc(tomorrow_1)
        self.assertEqual(
                (streak.getStreak(tomorrow_1), streak.best),
                (3, 3)
        )
        streak.inc(tomorrow_3)
        self.assertEqual(
                (streak.getStreak(tomorrow_3), streak.best),
                (1, 3)
        )

class TrackTest(TestCase):
    def setUp(self):
        self.user = User(name='superjom')
        #self.user.init()
        self.user.save()
        initDB()

    def test_Add(self):
        course = Course.objects.all()[0]
        chapter = Chapter.objects.all()[0]
        step = chapter.step_set.all()[0]

        track = Track(
            user = self.user,
            chapter = chapter,
            step = step
        )
        track.flush()
        print '.. track: ', track


class UserTest(TestCase):
    def setUp(self):
        self.user = User(name='superjom')
        self.user.save()

    def test_point(self):
        print 'first point: ', self.user.point
        print 'first point: ', self.user.point
        print 'first point: ', self.user.point
        print 'first point: ', self.user.point
        self.user.point.inc(1)
        print 'first inc: ', self.user.point
        self.user.point.inc(1)
        print 'inc: ', self.user.point



