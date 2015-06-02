from api.mid_level import Remote, Compiled

class Problem(Remote, Compiled):
    executable_name = "mybinary"

    def __init__(self):
        self.secret = "asdf"
