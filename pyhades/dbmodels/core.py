from peewee import Proxy, Model

proxy = Proxy()

SQLITE = 'sqlite'
MYSQL = 'mysql'
POSTGRESQL = 'postgresql'


class BaseModel(Model):

    @classmethod
    def read(cls, id:int) -> dict:
        r"""
        Select a single record

        You can use this method to retrieve a single instance matching the given query. 

        This method is a shortcut that calls Model.select() with the given query, but limits the result set to a single row. 
        Additionally, if no model matches the given query, a DoesNotExist exception will be raised.

        **Parameters**

        * **id:** (int), Record ID

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (list) row serialized}

        """
        result = dict()
        data = dict()
        query = cls.select().where(cls.id == id).get_or_none()

        if query:
            
            message = f"You have got id {id} successfully"
            data.update(query.serialize())

            result.update(
                {
                    'message': message, 
                    'data': data
                }
            )
            return result

        message = f'ID {id} not exist into database'       
        result.update(
                {
                    'message': message, 
                    'data': data
                }
            )

        return result

    @classmethod
    def read_all(cls):
        r"""
        Select all records

        You can use this method to retrieve all instances matching in the database. 

        This method is a shortcut that calls Model.select() with the given query.

        **Parameters**

        **Returns**

        * **result:** (dict) --> {'message': (str), 'data': (list) row serialized}
        """

        # result = dict()
        data = list()
        
        try:
            data = [query.serialize() for query in cls.select()]

            return data

        except Exception as _err:

            return data

    @classmethod
    def put(cls, id:int, **fields)-> dict:
        r""""
        Update a single record

        Once a model instance has a primary key, you UPDATE a field by its id. 
        The model's primary key will not change:
        """
        result = dict()
        data = dict()
        
        if cls.check_record(id):

            query = cls.update(**fields).where(cls.id == id)
            query.execute()
            message = f"You updated ID {id} successfuly"
            query = cls.select().where(cls.id == id).get_or_none()
            result.update(
                {
                    'message': message,
                    'data': query.serialize()
                }
            )

            return result

        message = f"ID {id} not exist into database"

        result.update(
            {
                'message': message,
                'data': data
            }
        )

        return result

    @classmethod
    def delete(cls, id:int):
        r"""
        Delete record from database including dependencies
        """
        if cls.check_record(id):
        
            query = super().delete().where(cls.id==id)
            query.execute()

            return {'message': f"You have deleted id {id} from database"}

        return {'message': f"id {id} not exist into database"}

    @classmethod
    def check_record(cls, id:int)->bool:
        r"""
        Verify if a record exist by its id

        **Parameters**

        * **id:** (int) Record ID

        **Returns**

        * **bool:** If True, so id record exist into database
        """
        query = cls.get_or_none(id=id)
        if query is not None:

            return True
        
        return False


    class Meta:
        database = proxy