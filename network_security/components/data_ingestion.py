from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo

from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from urllib.parse import quote_plus
import certifi  # Crucial for stable TLS connection with Atlas

load_dotenv()

# Match the exact programmatic string logic from test_mongo.py
username = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASS") or ""
password = quote_plus(raw_password)

MONGO_DB_URL = f"mongodb+srv://{username}:{password}@ac-jisg9r6.flqalgx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """
        Read data securely from MongoDB Atlas and convert it into a pandas DataFrame.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(f"Connecting to DB: {database_name} | Collection: {collection_name}")
            
            # Secure connection via certifi CA bundle
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=certifi.where()
            )

            collection = self.mongo_client[database_name][collection_name]
            
            # Extract data records
            documents = list(collection.find())
            
            # Early validation warning if configuration strings point to empty slots
            if len(documents) == 0:
                raise ValueError(
                    f"Fetched 0 documents from Database: '{database_name}', Collection: '{collection_name}'. "
                    f"Check if names match your cluster exactly."
                )

            df = pd.DataFrame(documents)

            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis=1)

            df.replace({"na": np.nan}, inplace=True)
            
            logging.info(f"Successfully loaded DataFrame with shape: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = (
                self.data_ingestion_config.feature_store_file_path
            )

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(
                feature_store_file_path,
                index=False,
                header=True
            )
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            # Dynamically reference ratio constraint from your config setup
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            train_file_path = self.data_ingestion_config.train_file_path
            test_file_path = self.data_ingestion_config.test_file_path

            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)

            logging.info("Train and test data split completed.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion.")

            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            logging.info(f"Data ingestion completed successfully. Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
