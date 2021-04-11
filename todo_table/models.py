from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from uuid import uuid4

KEY = "Yfk09rYCg/jQ28U0g7TfVyayPPShzO1c9FhOpaJ+wOqUqhTkR2Xi8D65CwLd4WmQcS+55i0fnH1CiTibdW3KYw=="
PARTITION_KEY = "todo"


class TodoDatabase:

    instance = None

    def __init__(self):
        if not TodoDatabase.instance:
            self.table_name = 'todostable'
            self.table_service = TableService(
                account_name='maheshsdcard', account_key=KEY)
            self.table_service.create_table(self.table_name)
            TodoDatabase.instance = self
        else:
            raise Exception("Singleton")

    @staticmethod
    def getInstance():
        if TodoDatabase.instance == None:
            TodoDatabase()
        return TodoDatabase.instance


def add_todo(title, description='', completed=False):
    client: TableService = TodoDatabase.getInstance().table_service
    return client.insert_entity('todostable', {'RowKey': str(
        uuid4()), 'title': title, 'description': description, 'completed': completed, 'PartitionKey' : 'todostable'})


def get_all_todo():
    client: TableService = TodoDatabase.getInstance().table_service
    return list(client.query_entities('todostable'))


def update_todo(id):
    client: TableService = TodoDatabase.getInstance().table_service
    el = client.get_entity('todostable','todostable',id)
    el.completed = True
    client.update_entity('todostable',el)


def delete_todo(id):
    client: TableService = TodoDatabase.getInstance().table_service
    client.delete_entity('todostable','todostable',id)
