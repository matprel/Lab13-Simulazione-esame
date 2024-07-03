from database.DB_connect import DBConnect
from model.avvistamento import Avvistamento
from model.stato import Stato


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """ select distinct(year(s.`datetime`)) as anno
                    from sighting s """
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getForme(anno):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """ select distinct(s.shape) as forma
                    from sighting s 
                    where s.shape != "" and year(s.`datetime`) = %s"""
        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAvvistamenti(forma, anno):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """ SELECT n.state1, n.state2 , count(*) as N
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2
                """
        cursor.execute(query, (anno, forma))

        for row in cursor:
            result.append((row['state1'],row['state2'], row["N"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStati():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)

        query = """ select *
                    from state s  """
        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result
