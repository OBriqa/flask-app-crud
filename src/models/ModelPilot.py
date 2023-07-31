from database.db import get_connection
from .entities.Pilot import Pilot
from utils.Format import PAGE_ELEMENTS, OK

class ModelPilot():

    @classmethod
    def get_attributes(self):
        return Pilot.get_atributtes()
    
    @classmethod
    def get_headings(self):
        return Pilot.get_headings()
    
    @classmethod
    def get_id(self):
        return Pilot.get_id()
    
    @classmethod
    def get_numElements(self, query):
        numElements = 0
        conn = get_connection()
        with conn.cursor() as cursor:
            if len(query) > 0:
                q = f"""SELECT count(*) FROM pilot 
                        WHERE   
                            nomP            {query['nomP-op']}          %s AND
                            dataN::text     {query['dataN-op']}         %s AND
                            nacionalitat    {query['nacionalitat-op']}  %s
                    """
                cursor.execute(q, (query['nomP'], query['dataN'], query['nacionalitat']))
            else:
                q = 'SELECT count(*) FROM pilot'
                cursor.execute(q)

            numElements = cursor.fetchone()[0]

        conn.close()
        return numElements
    
    @classmethod
    def get_pilots(self, num_page, order, query):

        try:
            pilots = []
            conn = get_connection()
            with conn.cursor() as cursor:
                if len(query) > 0:
                    q = f"""SELECT * FROM pilot 
                            WHERE   
                                nomP            {query['nomP-op']}          %s AND
                                dataN::text     {query['dataN-op']}         %s AND
                                nacionalitat    {query['nacionalitat-op']}  %s
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (query['nomP'], query['dataN'], query['nacionalitat'], PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                else:
                    q = f"""SELECT * FROM pilot 
                            ORDER BY 
                                {order} ASC LIMIT %s OFFSET (%s - 1) * %s"""
                    cursor.execute(q, (PAGE_ELEMENTS, num_page, PAGE_ELEMENTS))
                
                result = cursor.fetchall()

                for row in result:
                    pilot = Pilot(row[0], row[1], row[2])
                    pilots.append(pilot.to_JSON())

            conn.close()
            return pilots, OK
        
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_pilot(self, nomP):

        try:
            pilot = None
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "SELECT * FROM pilot WHERE nomP = %s"
                cursor.execute(q, (nomP,))
                row = cursor.fetchone()

                if row != None:
                    pilot = Pilot(row[0], row[1], row[2])
                    pilot = pilot.to_JSON()

            conn.close()
            return pilot, OK
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_pilot(self, Pilot):

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "INSERT INTO pilot(nomP, dataN, nacionalitat) VALUES (%s, %s, %s)"
                cursor.execute(q, (Pilot.nomP, Pilot.dataN, Pilot.nacionalitat))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))
        
    @classmethod
    def update_pilot(self, Pilot):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "UPDATE pilot SET dataN = %s, nacionalitat = %s WHERE nomP = %s"
                cursor.execute(q, (Pilot.dataN, Pilot.nacionalitat, Pilot.nomP))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))
        
    @classmethod
    def delete_pilot(self, nomP):
        
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                q = "DELETE FROM pilot WHERE nomP = %s"
                cursor.execute(q, (nomP,))
                affected_rows = cursor.rowcount

                conn.commit()

            conn.close()
            return affected_rows, OK
        
        except Exception as ex:
            return 0, str(Exception(ex))