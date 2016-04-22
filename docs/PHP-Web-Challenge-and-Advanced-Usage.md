We will now create a PHP SQL injection challenge. This will showcase how to structure your
web challenges and use SQLite databases with your challenges.

Start with making an empty directory named `sqlinject`.
Within this directory, make another directory named `webroot`. This is where
we will place our html and php files.

At `webroot/index.html`, place the following:

```html
<!doctype html>
<html>
<head>
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <div class="panel panel-primary" style="margin-top:50px">
                <div class="panel-heading">
                    <h3 class="panel-title">Log In</h3>
                </div>
                <div class="panel-body">
                    <form action="login.php" method="POST">
                        <fieldset>
                            <div class="form-group">
                                <label for="username">Username:</label>
                                <input type="text" id="username" name="username" class="form-control">
                            </div>
                            <div class="form-group">
                                <label for="password">Password:</label>
                                <div class="controls">
                                    <input type="password" id="password" name="password" class="form-control">
                                </div>
                            </div>

                            <input type="hidden" name="debug" value="0">

                            <div class="form-actions">
                                <input type="submit" value="Login" class="btn btn-primary">
                            </div>
                        </fieldset>
                    </form>
                </div>
            </div>
            <a href="login.phps">login.php source code</a>
        </div>
    </div>
</div>
</body>
</html>
```

This is just a basic login form that submits to `login.php`, which we'll create below.
The web page above also links to the source code at `login.phps`. The extension is `.phps`
so that we can serve the file normally instead of executing it.

At `webroot/login.php` and `webroot/login.phps`, place:

```php
<?php
  include "config.php";
  $con = new SQLite3($database_file);

  $username = $_POST["username"];
  $password = $_POST["password"];
  $debug = $_POST["debug"];
  $query = "SELECT * FROM users WHERE name='$username' AND password='$password'";
  $result = $con->query($query);
  if (intval($debug)) {
    echo "<pre>";
    echo "username: ", htmlspecialchars($username), "\n";
    echo "password: ", htmlspecialchars($password), "\n";
    echo "SQL query: ", htmlspecialchars($query), "\n";
    echo "</pre>";
  }

  $row = $result->fetchArray();

  if ($row) {
    echo "<h1>Logged in!</h1>";
    echo "<p>Your flag is: $FLAG</p>";
  } else {
    echo "<h1>Login failed.</h1>";
  }
?>
```

This has a vulnerable query string that can be injected into. At the top, we included `config.php`.
This will store some information that we don't want to display to the users.

So, put the following code in `webroot/config.php`.

```php
<?php
$FLAG = "{{flag}}";
$database_file = "../users.db";
?>
```

And that's it for the `webroot` directory. Now that our website is set up,
we have to create our `problem.json` and `challenge.py`.

For our `problem.json`, let's use the following:

```json
{
  "name": "SQL Injection 1",
  "category": "Web Exploitation",
  "pkg_dependencies": ["php5-sqlite"],
  "description": "There is a website running at http://{{server}}:{{port}}. Try to see if you can login!",
  "score" : 40,
  "hints": [],
  "author": "Your name here",
  "organization": "Example"
}
```

Notice the `pkg_dependencies` field, where you can specify `apt` packages to install along with your problem.
In order to run this problem, we're going to need the `php5-sqlite` package installed. Be sure to install this
manually if you wish to test the deployment before packaging.

Finally, let's write our `challenge.py`. We'll again use the Inheritance API - this time
extending the `PHPApp` class.

```python
from hacksport.problem import PHPApp, ProtectedFile, files_from_directory
import sqlite3

class Problem(PHPApp):
  files = files_from_directory("webroot/") + [ProtectedFile("users.db")]
  php_root = "webroot/"

  def setup(self):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE users (name text, password text, admin integer);')
    c.execute('''INSERT INTO users VALUES ('admin', 'pbkdf2:sha1:1000$bTY1abU0$5503ae46ff1a45b14ff19d5a2ae08acf1d2aacde', 1)''')
    conn.commit()
    conn.close()
```

We make use of the `files_from_directory` function to load all files from the `webroot` directory.
Additonally, we want the database to be a `ProtectedFile`, so that only our problem user can read it.

We specify the `php_root` field so that the `PHPApp` class knows where to serve files from.

Finally, we override the `setup` function, which is the last to be ran during
instance generation. In here, we create the SQLite3 database using the python API.

We can now run the testing, packaging, and installation steps as demonstrated in the
previous examples.

Continue to the bundle example [here](Bundling and Deploying).