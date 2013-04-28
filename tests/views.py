__all__ = (
    'UserInfoPageTest',
)
from codepku.users.views.userinfo import UserInfoPage
from codepku.users.models import *
from codepku.utils import Storage
from codepku.lesson.models import Step
from codepku.lesson.tests import DBIniter
from codepku.record.models import UserRecord

from django.test import TestCase
from django.test.client import Client

class UserInfoPageTest(TestCase):
    def setUp(self):
        DBIniter.init_lesson()
        self.user = DBIniter.init_user()
        self.stepid = DBIniter.init_tips()
        # save to step1
        DBIniter.init_badge()

        self.userid = self.user.id
        self.post = Storage()
        post = self.post
        post.userid = self.userid
        post.cmd = 'print "hello"'
        stepid = Step.objects.all()[0].id
        post.stepId = stepid
        post.nextStepId = self.stepid

        self.client = Client()



    def test_getData(self):
        request = Storage()
        session = Storage()
        session.userid = self.user.id
        session.username = 'superjom'
        session.usertype = 'sina'
        request.session = session
        u = UserInfoPage()
        data = u.getPoint(self.user)
        self.assertNotEqual(data, None, 'something wrong with user info')

    def test_get(self):
        # ------ django hack ----
        # Setu.p Test User
        from django.contrib.auth.models import User as AdminUser
        AdminUser.objects.create_superuser(
            'test',
            'test@test.org',
            'test')
        self.client.login(username='test', password='test')

        session = self.client.session
        session['userid'] = self.user.id
        session.save()
    
        # init record
        res = self.client.post('/lesson/update-process', {
            'nextStepId': self.stepid,
            'stepId': 1,
            'cmd': 'print "hello"'
        })
        records = UserRecord.objects.all()
        self.assertEqual(len(records) >= 1, True, "userrecord not saved")
        # test_user_point
        user = User.objects.get(id=self.userid)
        point = user.point
        print '## point: ', point
        self.assertEqual(
            (point.today, point.best, point.total), 
             (1, 1, 1), "wrong with user point inc")

        # streak
        streak = user.streak
        print '##> streak:', streak
        self.assertEqual(
            (streak.streak, streak.best),
            (1, 1), "wrong with streak")

        # badge
        badge = user.badges.all()[0]
        self.assertNotEqual(badge, None, "badge not added successfully")

    def test_track(self):
        user = User.objects.get(id=self.userid)
        # ------ django hack ----
        # Setu.p Test User
        from django.contrib.auth.models import User as AdminUser
        AdminUser.objects.create_superuser(
            'test',
            'test@test.org',
            'test')
        self.client.login(username='test', password='test')
        # ---------end django hack ------------
        session = self.client.session
        session['userid'] = self.userid 
        session.save()

        self.client.post('/lesson/update-process', {
            'nextStepId': self.stepid,
            'stepId': 1,
            'cmd': 'print "hello"'
        })
        # track
        tracks = user.track_set.all()
        print 'tracks: ', tracks

        self.client.post('/lesson/update-process', {
            'nextStepId': self.stepid,
            'stepId': 2,
            'cmd': 'print "hello"'
        })
        # track
        tracks = user.track_set.all()
        print 'tracks: ', tracks

        self.client.post('/lesson/update-process', {
            'nextStepId': self.stepid,
            'stepId': 3,
            'cmd': 'print "hello"'
        })
        # track
        tracks = user.track_set.all()
        print 'tracks: ', tracks

        self.client.post('/lesson/update-process', {
            'nextStepId': self.stepid,
            'stepId': 3,
            'cmd': 'print "hello"'
        })
        # track
        tracks = user.track_set.all()
        print 'tracks: ', tracks


        """
        res = self.client.get('/users/userinfo', {
        })
        print res
        """

