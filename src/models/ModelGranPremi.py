from database.db import get_connection
from .entities.GranPremi import GranPremi
from utils.Format import PAGE_ELEMENTS, OK

class ModelGranPremi():

    @classmethod
    def get_attributes(self):
        return GranPremi.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return GranPremi.get_headings()
    
    @classmethod
    def get_id(self):
        return GranPremi.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM granPremi 
                        WHERE   
                            nomGP       {query['nomGP-op']}     %s AND
                            circuit     {query['circuit-op']}   %s AND
                            situat      {query['situat-op']}    %s
                    """
                cursor.execute(q, (query['nomGP'], query['circuit'], query['situat']))
            else:
                q = 'SELECT count(*) FROM granPremi'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements

    @classmethod
    def get_gransPremis(self, num_page, order, query):

        try:
            granspremis = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM granPremi 
                            WHERE   
                                nomGP       {query['nomGP-op']}     %s AND
                                circuit     {query['circuit-op']}   %s AND
                                situat      {query['situat-op']}    %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['nomGP'], query['circuit'], query['situat'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM granPremi 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    granPremi = GranPremi(row[0], row[1], row[2])
                    granspremis.append(granPremi.to_JSON())

            conn.close()
            return granspremis, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_granPremi(self, nomGP):

        try:
            granPremi = None
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "SELECT * FROM granPremi WHERE nomGP = %s"
                cursor.execute(q, (nomGP,))
                row = cursor.fetchone()

                if row != None:
                    granPremi = GranPremi(row[0], row[1], row[2])
                    granPremi = granPremi.to_JSON()

            conn.close()
            return granPremi, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_granPremi(self, GranPremi):

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "INSERT INTO granPremi(nomGP, circuit, situat) VALUES (%s, %s, %s)"
                cursor.execute(q, (GranPremi.nomGP, GranPremi.circuit, GranPremi.situat))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))
        
    @classmethod
    def update_granPremi(self, GranPremi):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "UPDATE granPremi SET circuit = %s, situat = %s WHERE nomGP = %s"
                cursor.execute(q, (GranPremi.circuit, GranPremi.situat, GranPremi.nomGP))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))        

    @classmethod
    def delete_granPremi(self, nomGP):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "DELETE FROM granPremi WHERE nomGP = %s"
                cursor.execute(q, (nomGP,))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))