from database.db import get_connection
from .entities.Temporada import Temporada
from utils.Format import PAGE_ELEMENTS, OK

class ModelTemporada():

    @classmethod
    def get_attributes(self):
        return Temporada.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Temporada.get_headings()
    
    @classmethod
    def get_id(self):
        return Temporada.get_id() 

    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM temporada 
                        WHERE   
                            anyT::text          {query['anyT-op']}                  %s AND
                            pilotCampio         {query['pilotCampio-op']}           %s AND
                            constructorCampio   {query['constructorCampio-op']}     %s
                    """
                cursor.execute(q, (query['anyT'], query['pilotCampio'], query['constructorCampio']))
            else:
                q = 'SELECT count(*) FROM temporada'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements    

    @classmethod
    def get_temporades(self, num_page, order, query):

        try:
            temporades = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM temporada
                            WHERE   
                                anyT::text          {query['anyT-op']}                  %s AND
                                pilotCampio         {query['pilotCampio-op']}           %s AND
                                constructorCampio   {query['constructorCampio-op']}     %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    
                    print(q)
                    cursor.execute(q, (query['anyT'], query['pilotCampio'], query['constructorCampio'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM temporada 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    temporada = Temporada(row[0], row[1], row[2])
                    temporades.append(temporada.to_JSON())

            conn.close()
            return temporades, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_temporada(self, anyT):

        try:
            temporada = None
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "SELECT * FROM temporada WHERE anyT = %s"
                cursor.execute(q, (anyT,))
                row = cursor.fetchone()

                if row != None:
                    temporada = Temporada(row[0], row[1], row[2])
                    temporada = temporada.to_JSON()

            conn.close()
            return temporada, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_temporada(self, Temporada):

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "INSERT INTO temporada(anyT, pilotCampio, constructorCampio) VALUES (%s, %s, %s)"
                cursor.execute(q, (Temporada.anyT, Temporada.pilotCampio, Temporada.constructorCampio))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))
        
    @classmethod
    def update_temporada(self, Temporada):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "UPDATE temporada SET pilotCampio = %s, constructorCampio = %s WHERE anyT = %s"
                cursor.execute(q, (Temporada.pilotCampio, Temporada.constructorCampio, Temporada.anyT))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))

    @classmethod
    def delete_temporada(self, anyT):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "DELETE FROM temporada WHERE anyT = %s"
                cursor.execute(q, (anyT,))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))