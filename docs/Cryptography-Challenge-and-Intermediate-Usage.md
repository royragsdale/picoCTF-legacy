The previous binary challenge was quite simple to create. It did not require
any random variables, additional files, source code templating, or custom
setup commands. These things are however achievable using the Inheritance
API, as you'll see in the following few challenges.

We will now write a cryptography challenge in which each instance has a unique
plaintext and encryption key. As before, the first step is to make a new directory.
Below is the full source code for our challenge. It doesn't need to be edited,
so let's place it directly in `ecb.py`.

```python
#!/usr/bin/python2
from Crypto.Cipher import AES
import os, sys

flag = open("flag", "r").read()
key = open("key", "r").read().strip()

welcome = """
{{welcome_message}}
"""

def encrypt():
  cipher = AES.new(key.decode('hex'), AES.MODE_ECB)
  return cipher.encrypt(flag).encode("hex")

# flush output immediately
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
print welcome
print "KEY: " + key
print "MESSAGE: " + encrypt()
```

Both the flag and the encryption key will be read from a file. This is so that
we can safely distribute the source code to the users without revealing the
sensitive information. The welcome message, however, is going to be templated
with whatever we specify in our `challenge.py`, as you'll see below. As before,
we will declare a variable named Problem, but this time we will use the
Inheritance API.

```python
from hacksport.problem import Remote, ProtectedFile
import string

class Problem(Remote):
    program_name = "ecb.py"
    files = [ProtectedFile("flag"), ProtectedFile("key")]

    def initialize(self):
        # generate random 32 hexadecimal characters
        self.enc_key = ''.join(self.random.choice(string.digits + 'abcdef') for _ in range(32))

        self.welcome_message = "Welcome to Secure Encryption Service version 1.{}".format(self.random.randint(0,10))
```

Let's take a look at what's going on. We created a class named Problem that extends
from the Inheritance API class Remote. The Remote class handles setting up a listening server
on a randomized port for you; all we must do is specify the `program_name` to execute when
receiving a connection.

The `files` list specifies which files we want to copy to the deployment directory. This list
must contain `File` objects from our API. `ProtectedFile` makes the file only readable by
our script. To read more about our `File` classes, check out the [File Specification](File Class Spec).
By default, `Remote` will copy the files we specify in `program_name`, so we can safely exclude that file
from our files list.

Next, we override the `initialize` function. This function is the first to run during instance
generation, so this is where we create some random variables. By doing this, we introduce `enc_key`
and `welcome_message` to the templating scope.

You may have noticed that we used `self.random`, but we never declared this variable. This is because
the Inheritance API introduces this for us, along with other useful fields. **Be sure to always use
the `self.random` object as your source of randomness.** You can read the
*Usage Tips* section of the [challenge.py Specification](Challenge.py) to learn more
about this.

After the API runs `initialize`, the templating step happens. Every file in your
problem directory will be automatically templated using the variables defined in
`challenge.py`. Thus, in order to correctly place the encryption key and flag in their
appropriate files, we should take advantage of the templating step. Let's create a file named
`flag` containing `{{flag}}` and a file named `key` containing `{{enc_key}}`.

Now all that is left is to make our `problem.json` file. As shown below, we can also use
templating in our description.

```json
{
  "name": "ECB Encryption",
  "category": "Cryptography",
  "description": "There is a crypto service running at {{server}}:{{port}}. We were able to recover the source code, which you can download at {{url_for(\"ecb.py\")}}.",
  "hints": [],
  "score" : 70,
  "author": "Your name here",
  "organization": "Example"
}
```

In the description, we have templated `{{server}}` and `{{port}}`. These are both implicitly
set by the Inheritance API. Additionally, we have templated `{{url_for('ecb.py')}}`. This will
generate a download link for this file to distribute to the participants. Remeber that it will
serve the templated version of this file, so the `welcome_message` will already be in the source.
This is why we didn't template the flag and key into the source code.

Now our problem is ready to be tested. As described on the
[Binary Exploitation Example](Simple Buffer Overflow Challenge), we can run
`sudo shell_manager deploy -d directory_name` to generate a test instance,
then run `sudo shell_manager package directory_name` to package it as a `.deb`.

Click [here](PHP Web Challenge and Advanced Usage) to continue to the next example problem.