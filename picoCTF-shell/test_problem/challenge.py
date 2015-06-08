from hacksport.problem import Remote, Compiled

class Problem(Remote, Compiled):
    program_name = "mybinary"
    makefile = "Makefile"

    def __init__(self):
        self.secret = "asdf"
