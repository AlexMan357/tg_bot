from database.utils.CRUD import CRUDInterface
from database.common.models import database_history, History

database_history.connect()
database_history.create_tables([History])

crud = CRUDInterface()

# if __name__ == '__main__':
#     crud()
