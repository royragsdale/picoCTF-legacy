from test_problem import challenge
from api.utility import generate
from os import chdir

chdir("test_problem")
print(generate(challenge.Problem, "asdf"))
