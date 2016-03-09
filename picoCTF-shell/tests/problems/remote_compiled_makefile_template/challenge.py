from hacksport.problem import Remote, Compiled, File, ExecutableFile, ProtectedFile

class Problem(Remote, Compiled):
    program_name = "mybinary"
    makefile = "Makefile"
    files = [File("mybinary.c"), ProtectedFile("flag.txt")]
    secret = "test"

    def __init__(self):
        self.lucky = self.random.randint(0, 1000)
