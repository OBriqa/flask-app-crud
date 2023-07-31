from database.db import get_connection
from .entities.Pais import Pais
from utils.Format import PAGE_ELEMENTS, OK

class ModelPais():

    @classmethod
    def get_atributtes(self):
        return Pais.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Pais.get_headings()
    
    @classmethod
    def get_id(self):
        return Pais.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM pais 
                        WHERE   
                            codi    {query['codi-op']}      %s AND
                            nom     {query['nom-op']}       %s
                    """
                cursor.execute(q, (query['codi'], query['nom']))
            else:
                q = 'SELECT count(*) FROM pais'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements    

    @classmethod
    def get_paissos(self, num_page, order, query):
        
        try:
            paissos = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM pais 
                            WHERE   
                                codi    {query['codi-op']}      %s AND
                                nom     {query['nom-op']}       %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['codi'], query['nom'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM pais 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    pais = Pais(row[0], row[1])
                    paissos.append(pais.to_JSON())

            conn.close()
            return paissos, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_pais(self, codi):
        try:
            pais = None
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "SELECT * FROM pais WHERE codi = %s"
                cursor.execute(q, (codi,))
                row = cursor.fetchone()

                if row != None:
                    pais = Pais(row[0], row[1])
                    pais = pais.to_JSON()

            conn.close()
            return pais, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_pais(self, Pais):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "INSERT INTO pais(codi, nom) VALUES (%s, %s)"
                cursor.execute(q, (Pais.codi, Pais.nom))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))
        
    @classmethod
    def update_pais(self, Pais):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "UPDATE pais SET nom = %s WHERE codi = %s"
                cursor.execute(q, (Pais.nom, Pais.codi))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_pais(self, codi):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "DELETE FROM pais WHERE codi = %s"
                cursor.execute(q, (codi,))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))