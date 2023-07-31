from database.db import get_connection
from .entities.Participa import Participa
from utils.Format import PAGE_ELEMENTS, OK

class ModelParticipa():
    
    @classmethod
    def get_atributtes(self):
        return Participa.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Participa.get_headings()
    
    @classmethod
    def get_id(self):
        return Participa.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM participa 
                        WHERE   
                            nomP            {query['nomP-op']}      %s AND
                            anyT::text      {query['anyT-op']}      %s
                    """
                cursor.execute(q, (query['nomP'], query['anyT']))
            else:
                q = 'SELECT count(*) FROM participa'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements
    
    @classmethod
    def get_participants(self, num_page, order, query):
        
        try:
            participants = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM participa 
                            WHERE   
                                nomP            {query['nomP-op']}      %s AND
                                anyT::text      {query['anyT-op']}      %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['nomP'], query['anyT'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM participa 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    constructor = Participa(row[0], row[1])
                    participants.append(constructor.to_JSON())

            conn.close()
            return participants, OK
        
        except Exception as ex:
            raise Exception(ex)