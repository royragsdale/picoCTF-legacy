# File Classes

To specify which files to copy into your deployment directory, you must populate the
`files` list with `File` objects. This page describes the various types of `File`s
and how they can be used.

### `File(path, permissions=0o664, user=None, group=None)`

Using the `File` constructor gives you the most control over how the file is copied.
Specifying only the path will copy the file with the most common permissions and set
the owner and group to the `DEFAULT_USER`. If `user` or `group` are set to a string,
the files will be copied with that user or group ownership.

### `ProtectedFile(path, permissions=0o440)`

The `ProtectedFile` constructor is a wrapper around `File` that provides a mechanism
for protecting files until privileges are escalated. For example, creating a file
with `ProtectedFile("flag.txt")` will make flag.txt only readable after escalating
privileges.

### `ExecutableFile(path, permissions=0o2755)`

The `ExecutableFile` constructor is a wrapper around `File` that will setup the
file to be executable and able to escalate privileges. This is most useful for
binary exploitation challenges, where escalating privileges to read the flag
is a common solution method.

### `files_from_directory(directory, recurse=True, permissions=0o664)`

The `files_from_directory` function returns a list of `File` objects representing
all files in the specified directory. Although the permissions are controllable
with this function, the ownership is not.