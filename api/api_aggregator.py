__author__ = "Peter Chapman"
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumely", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"

#!/usr/bin/env python
from datetime import datetime
import json
import time
import logging

from bson import ObjectId
from common import db
from common import cache
import scoreboard

end = datetime(2020, 5, 7, 3, 59, 59)


def load_group_scoreboards():
    for group in list(db.groups.find()):
        scoreboard.load_group_scoreboard(group)

LOG_FILENAME = 'agg_output.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
logging.debug("\nAGGREGATOR START")
while True:
    load_group_scoreboards()
    time.sleep(30)
