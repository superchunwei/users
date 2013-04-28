<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>用户信息</title>
</head>
<body>

<h2>username: {{username}}</h2>
<h2>avater: {{avater}}</h2>
<h2>usertype: {{usertype}}</h2>
<h2>badges:</h2>
<ul>
    {% for b in badges %}
    <li>name: {{b.name}}--url: {{b.url}}</li>
    {% endfor %}
</ul>

<h2>point:</h2>
<ul>
    <li>today: {{point.today}}</li>
    <li>best: {{point.best}}</li>
    <li>total: {{point.total}}</li>
</ul>

<h2>streak:</h2>
<ul>
    <li>streak: {{streak.streak}}</li>
    <li>best: {{streak.best}}</li>
</ul>

<h2>activities:</h2>
{% for a in activities %}
<ul>
    <li>content: {{a.content}}</li>
    <li>date: {{a.date}}</li>
</ul>
{% endfor %}

<h2>tracks</h2>
{% for t in tracks %}
<ul>
    <li>course_name: {{t.course_name}}</li>
    <li>chapter_name: {{t.chapter_name}}</li>
    <li>step_no: {{t.step_no}}</li>
    <li>step_len: {{t.step_len}}</li>
</ul>
{% endfor %}
    
</body>
</html>
