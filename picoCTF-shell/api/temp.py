import random
import abc
import hashlib
import string

class Challenge(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setup(self):
        pass

    def initialize(self):
        pass

    def service(self):
        pass

    def generate_flag(self):
        return "".join([self.random.choice(list(string.hexdigits.lower())) for i in range(64)])

class Remote(Challenge):
    def setup(self):
        pass

    def setup_remote(self):
        print("setup_remote -", self.random.randint(1,500))


class Compiled(Challenge):
    def setup(self, rand):
        pass

    def setup_compiled(self):
        print("setup_compiled -", self.random.randint(1, 500))

class Problem(Remote, Compiled):
    def __init__(self):
        print(self.random.randint(1,500))

def seeded_meta(seed):
    class ChallengeMeta(abc.ABCMeta):
        def __new__(cls, name, bases, attr):
            attributes = dict(attr)
            attributes['random'] = random.Random(seed)
            return super().__new__(cls, name, bases, attributes)
    return ChallengeMeta

def generate(Problem, pid, tid):
    seed = hashlib.md5((pid+tid).encode('utf-8')).hexdigest()
    Problem = seeded_meta(seed)(Problem.__name__, Problem.__bases__, Problem.__dict__)
    p = Problem()
    p.initialize()

    if isinstance(p, Compiled):
        p.setup_compiled()
    if isinstance(p, Remote):
        p.setup_remote()
    p.setup()

    p.random.seed(seed)
    print(p.generate_flag())

generate(Problem, "afsd", "j;kl")
