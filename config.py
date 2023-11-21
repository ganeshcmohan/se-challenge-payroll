import os
from datetime import timedelta


class Config(object):
    DEBUG = True

    # local development use below mongo url
    MONGO_URI = os.environ.get(
        "MONGO_URI", "mongodb://payrolldb_2023:27017/payrolldb_2023"
    )
