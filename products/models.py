from django.db import models

# Momgodb imports
from pymongo import MongoClient

# Create your models here.


# connects a database
def get_database(dbname):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo

    CONNECTION = "<MONGODB:CONNECTION_LINK>"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION)

    # returns client connection str
    return client[dbname]
