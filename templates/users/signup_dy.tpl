<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User setup</title>
</head>
<body>
<h1>User Sign Up</h1>
<table>
<form method='POST' action='signup'> {% csrf_token %}
{{ form }}
<tr>
    <td><button type='submit'>Submit</button></td>
    <td><button type='cancel'>Cancel</button></td>
</tr>
</form>
<table>
</body>
</html>
