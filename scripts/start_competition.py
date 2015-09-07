import sys

sys.path.append("/vagrant/ctf-infrastructure/api")

import api

from datetime import datetime, timedelta

settings = api.config.get_settings()
settings["start_time"] = datetime.now()
settings["end_time"] = settings["start_time"] + timedelta(weeks=1)

api.config.change_settings(settings)

print("Started the competition")
