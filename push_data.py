import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")
MONGO_DB_url = os.getenv("URI")

print("USERNAME:", USERNAME)
print("PASSWORD loaded:", PASSWORD is not None)
print("URI loaded:", MONGO_DB_url is not None)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging.logger import network_security_logger


class network_dataExtract:

    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def cv_to_json_convertor(self, file_path):

        try:
            data = pd.read_csv(file_path)

            data.reset_index(drop=True, inplace=True)

            records = list(
                json.loads(data.T.to_json()).values()
            )

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_into_mongodb(self, records, database, collection):

        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_url,
                tlsCAFile=ca
            )

            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    file_path = 'Network_data/Data.csv'

    database = "ujjwal"

    collection = "network_data"

    networkobj = network_dataExtract()

    records = networkobj.cv_to_json_convertor(
        file_path=file_path
    )

    print("Number of records:", len(records))

    no_of_records = networkobj.insert_data_into_mongodb(
        records,
        database,
        collection
    )

    print("Records inserted:", no_of_records)
