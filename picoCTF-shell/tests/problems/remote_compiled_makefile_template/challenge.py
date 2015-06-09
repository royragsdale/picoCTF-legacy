from hacksport.problem import Remote, Compiled, File, ExecutableFile, ProtectedFile

class Problem(Remote, Compiled):
    program_name = "mybinary"
    makefile = "Makefile"

    def __init__(self):
        self.files = [File("mybinary.c"), ExecutableFile("mybinary"), ProtectedFile("flag.txt")]
        self.secret = "asdf"
        self.lucky = self.random.randint(0, 1000)
