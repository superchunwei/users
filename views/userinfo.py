# -*- coding: utf-8 -*-
"""
用户信息展示
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from codepku.utils import Storage, error404
from codepku.users.models import User, Badge

class UserInfoPage(TemplateView):
    """
    用户信息页面

    globals:
        self.user: <User>

    return data:
        {
            username : session['username'],
            avater: url,
            tracks: [ {   course: name, 
                        chapter: name, 
                        step: no, 
                        step_len: length of steps
                    } ],
            point: { today, best, total },
            streak: { streak, best },
            badges: [ { name,  url: image, }, ],
            activities: [ {date, content,} ],
        }
    """
    def get(self, request, *args, **kwargs):
        # TODO 传入那种信息
        data = self.getData(request)

        if data is None:
            return render(request, 'users/userinfo.tpl', data)
        else:
            return error404("get userinfo error")

    def getData(self, request):
        _session  = Storage(request.session)
        self.user = User.objects.get(id=_session.userid)

        try:
            return { 
                'username': _session.username,
                'avater': _session.avater,
                'usertype': _session.usertype,
                'badges' : self.getBadges(),
                'point' : self.getPoint(self.user),
                'streak' : self.getStreak(),
                'activities' : self.getActivities(), 
                'tracks': self.getTracks(),}
        except:
            return None

    # -------------------- details ---------------------------
    # -------------------- details ---------------------------
    def getBadges(self):
        """
        return a list of 
            [{name, url}, ... ]
        """
        badges = self.user.badge_set.order_by('no').all()
        res = []
        for b in badges:
            res.append({'name': b.name, 'url':b.url})
        return res

    def getPoint(self, user):
        """
        return a list of 
            {today, best, total}
        """
        point = user.point
        return {
            'today': point.getToday(),
            'best': point.getBest(),
            'total': point.getTotal(),
        }

    def getStreak(self):
        streak = self.user.streak
        return {
            'streak': streak.getStreak(),
            'best': streak.getBest(),
        }

    def getActivities(self):
        activities = self.user.activity_set.order_by('date').all()
        res = []
        for a in activities:
            res.append(
                { 'content': a.content,
                    'date': a.date, })
        return res

    def getTracks(self):
        tracks = self.user.treak_set.order_by('date').all()
        res = []
        for t in tracks:
            res.append( { 'course_name': t.course_name,
                    'chapter_name': t.chapter_name,
                    'step_no': t.step_no,
                    'step_len': t.step_len,
                    })
        return res
