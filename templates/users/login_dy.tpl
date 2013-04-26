<table>
<form method='POST' action='/users/login'> {% csrf_token %}
<div id='user-login-msg' style='text-align:center;color:orange;margin:10px auto;'></div>
    {{ form }} 
{% comment %}
<!-- button is not necessary, adding in template file -->
<tr>
    <td><button type='submit'>Submit</button></td>
    <td><button type='cancel'>Cancel</button></td>
</tr>
{% endcomment %}
</form>
<table>
