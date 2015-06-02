from test_problem import challenge
from api.utility import generate_instance
from os import chdir
from bson import json_util

chdir("test_problem")
service, flag = generate_instance(challenge.Problem, json_util.loads(open("problem.json").read()))
print(service)
print(flag)
