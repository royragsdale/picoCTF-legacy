__author__ = 'Collin Petty'
import tempfile
import os


def validate_dependencies():
    """Validate external dependencies.

    This function does NOT have to exist. If it does exist the runtime will call and execute it during api
    initialization. The purpose of this function is to verify that external dependencies required to auto-generate
    a problem are properly installed and configured on this system. Some common tasks that may be performed are
    checking that a certain program is installed (such as 'javac') and that it is executable. You may also want to
    verify that template files that the generator modifies exist in the templates/ directory. If any dependency
    check fails the function should print out the respective error message and return False. If all checks pass
    correctly the function should return True. If the function does not exist the API initializer will assume that
    all dependencies are met and will add the generator to the pre-fetched generator list assuming there is an
    auto-generated problem in the database that has the given generator set for it's 'generator' field.

    The following code demonstrates how to check that the java compiler (javac) is present on the system and can be
    executed by the current user.
    """
    print "DEPENDENCY CHECK - TEMPLATE.py (TEMPLATE)"
    javac_path = "/usr/bin/javac"  # This should have scope across the entire module but doesn't for template purposes
    if not os.path.exists(javac_path):
        print "ERROR - TEMPLATE - The specified java compiler (%s) does not appear to exist." % javac_path
        return False
    if not os.access(javac_path, os.X_OK):
        print "ERROR - TEMPLATE - javac is not executable by the python runtime."
        return False
    return True


def generate():
    """Generate an instance of the problem

    This is the function that is responsible for generating an instance of the auto-generated problem. The function
    has no concept of 'pid's or 'tid's. All generated files should use the tempfile module to build their output files
    and return a list of these files to the API for moving and renaming.

    Three values are returned as a tuple when generate() is called, the first value is a list of all user-facing
    files created by the auto-generator (there is typically only 1 output file such as a .class file, .xml file,
    etc etc). The second returned value is *either* the solution key or the name of a grader file (also created
    using the tempfile module). The ability to return a key was added after we saw that a lot of the graders being
    generated were simply checking if a passed value was equal to a given value. The problem's entry in the
    'problems' database will specify whether or not the 'grader' is a 'key' or 'file' for auto-generated problems
    (normal problems have the name of the grading script in this field). The third return value is the problem
    description (html). Any of the url links in it should be returned with '###file_X_url###' as their href value,
    where X is a number 1,2,3... representing the file in the return list (starts at 1 not 0). The API will move
    the temporary files returned in the list to the web server and replace these place holders with the proper paths.

    The following code generates a sample problem where a text file with a hard coded secret key is returned to a
    the API with a simple problem statement that demonstrates the description text replacement functionality.
    """
    key = "123456"
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    output.write("key = '%s'" % key)
    output.close()
    return [os.path.abspath(output.name)], key, """<p>Download <a href='###file_1_url###'>This file</a>\
     and get the secret key.</p>"""
