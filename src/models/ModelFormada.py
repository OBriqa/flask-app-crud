from database.db import get_connection
from .entities.Formada import Formada
from utils.Format import PAGE_ELEMENTS, OK

class ModelFormada():
    
    @classmethod
    def get_atributtes(self):
        return Formada.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Formada.get_headings()
    
    @classmethod
    def get_id(self):
        return Formada.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM formada 
                        WHERE   
                            anyT::text      {query['anyT-op']}      %s AND
                            nomGP           {query['nomGP-op']}     %s
                    """
                cursor.execute(q, (query['anyT'], query['nomGP']))
            else:
                q = 'SELECT count(*) FROM formada'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements
    
    @classmethod
    def get_formades(self, num_page, order, query):
        
        try:
            formades = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM formada 
                            WHERE   
                                anyT::text      {query['anyT-op']}      %s AND
                                nomGP           {query['nomGP-op']}     %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['anyT'], query['nomGP'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM formada 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    formada = Formada(row[0], row[1])
                    formades.append(formada.to_JSON())

            conn.close()
            return formades, OK
        
        except Exception as ex:
            raise Exception(ex)