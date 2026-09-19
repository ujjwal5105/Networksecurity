import os
import sys
import numpy as np
import pandas as pd

"""
defining common constants variable for traning pipeline
"""
TARGET_COLUMN: str = "result"
PIPELINE_NAME: str = "network_security"
ARTIFACTS_DIR: str = "artifacts"
FILE_NAME: str = "Data.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


"""
Data Ingestion relaateed constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "ujjwal"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

