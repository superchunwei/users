<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User setup</title>
</head>
<body>
<h1>User Sign Up</h1>
    <form method='post' action="/users/validate">
        <table>
            <tr>
                <td>Name</td>
                <td><input name='name' type="text" /></td>
            </tr>
            <tr>
                <td>email</td>
                <td><input name='email' type="text" /></td>
            </tr>
            <tr>
                <td>password</td>
                <td><input name='password' type="text" /></td>
            </tr>
            <tr>
                <td>repeat it</td>
                <td><input name='re-password' type="text" /></td>
            </tr>
            <tr>
                <td>gender</td>
                <td><input name='gender' type="text" /></td>
            </tr>
            <tr>
                <td>birth</td>
                <td><input name='birth' type="text" /></td>
            </tr>
            <tr>
                <td>work</td>
                <td><input name='work' type="text" /></td>
            </tr>
            <tr>
                <td></td>
                <td>
                    <button type='button'>Submit</button>
                    <button type='button'>Concel</button>
                </td>
            </tr>
        </table>
    </form>
</body>
</html>
