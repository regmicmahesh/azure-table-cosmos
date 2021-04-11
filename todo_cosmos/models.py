import logging
from uuid import uuid4

from azure.cosmos import CosmosClient, PartitionKey, ContainerProxy

ENDPOINT = "#"
KEY = "#"


db = None


class TodoDatabase:
    __instance = None

    @staticmethod
    def getInstance():
        if TodoDatabase.__instance == None:
            TodoDatabase()
        return TodoDatabase.__instance

    def __init__(self):
        if TodoDatabase.__instance == None:
            client = CosmosClient(ENDPOINT, KEY)
            database_name = 'TodoAppDatabase'
            self.database = client.create_database_if_not_exists(
                id=database_name)

            container_name = 'TodoAppContainer'
            self.client = self.database.create_container_if_not_exists(
                id=container_name, partition_key=PartitionKey(path="/id"), offer_throughput=400)
            TodoDatabase.__instance = self
        else:
            logging.fatal("Cannot call constructor directly from singleton.")


def add_todo(title, description='', completed=False):
    client: ContainerProxy = TodoDatabase.getInstance().client
    return client.create_item(body={'id': str(
        uuid4()), 'title': title, 'description': description, 'completed': completed})


def get_all_todo():
    client: ContainerProxy = TodoDatabase.getInstance().client
    return list(client.query_items("SELECT * from TodoAppContainer", enable_cross_partition_query=True))


def update_todo(id):
    client: ContainerProxy = TodoDatabase.getInstance().client
    el =  next(client.query_items(f'SELECT * FROM  TodoAppContainer c WHERE c.id="{id}"', enable_cross_partition_query=True))
    el['completed'] = True
    client.upsert_item(body=el) 

def delete_todo(id):
    client: ContainerProxy = TodoDatabase.getInstance().client
    client.delete_item(id,partition_key=id)
