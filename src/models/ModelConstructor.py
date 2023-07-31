from database.db import get_connection
from .entities.Constructor import Constructor
from utils.Format import PAGE_ELEMENTS, OK

class ModelConstructor():
    
    @classmethod
    def get_atributtes(self):
        return Constructor.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Constructor.get_headings()
    
    @classmethod
    def get_id(self):
        return Constructor.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM constructor 
                        WHERE   
                            nomC    {query['nomC-op']}      %s AND
                            seu     {query['seu-op']}       %s
                    """
                cursor.execute(q, (query['nomC'], query['seu']))
            else:
                q = 'SELECT count(*) FROM constructor'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements
    
    @classmethod
    def get_constructors(self, num_page, order, query):
        
        try:
            constructors = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM constructor 
                            WHERE   
                                nomC    {query['nomC-op']}      %s AND
                                seu     {query['seu-op']}       %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['nomC'], query['seu'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM constructor 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    constructor = Constructor(row[0], row[1])
                    constructors.append(constructor.to_JSON())

            conn.close()
            return constructors, OK
        
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_constructor(self, nomC):
        try:
            constructor = None
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "SELECT * FROM constructor WHERE nomC = %s"
                cursor.execute(q, (nomC,))
                row = cursor.fetchone()

                if row != None:
                    constructor = Constructor(row[0], row[1])
                    constructor = constructor.to_JSON()

            conn.close()
            return constructor, OK
        
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_constructor(self, Constructor):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "INSERT INTO constructor(nomC, seu) VALUES (%s, %s)"
                cursor.execute(q, (Constructor.nomC, Constructor.seu))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))

    @classmethod
    def update_constructor(self, Constructor):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "UPDATE constructor SET seu = %s WHERE nomC = %s"
                cursor.execute(q, (Constructor.seu, Constructor.nomC))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            raise Exception(ex)
  
    @classmethod
    def delete_constructor(self, nomC):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "DELETE FROM constructor WHERE nomC = %s"
                cursor.execute(q, (nomC,))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))