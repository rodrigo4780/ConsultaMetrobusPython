import os
import psycopg2
import reverse_geocoder as rg

class Base():
    def __init__(self):        
        self.DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
        self.DATABASE_USERNAME =  os.getenv('DATABASE_USERNAME', 'postgres')
        self.DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'localdb')
        self.DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
        self.DATABASE_PORT = os.getenv('DATABASE_PORT', 5434)
        print(self.DATABASE_USERNAME)

    def connection(self):
            conn = psycopg2.connect(database=self.DATABASE_NAME, 
                                    user=self.DATABASE_USERNAME, 
                                    password=self.DATABASE_PASSWORD, 
                                    host=self.DATABASE_HOST, 
                                    port=self.DATABASE_PORT)
            return conn

    def __execute_query__(self, query, values = None):
        
        conn = self.connection()        
        cur = conn.cursor()

        cur.execute(query, values)
        items = cur.fetchall()        
        cur.close()
        conn.close()
        
        return items 

    def insert_metrobus_data(self, records):
        conn = self.connection()        
        cur = conn.cursor()
        
        for record in records:
            print(record)
            coordinates = (record["position_latitude"], record["position_longitude"])
            alcaldia_id = self.get_id_alcaldia(coordinates)
            print("alcaldia id:", alcaldia_id)
            cur.execute(f"""
                        INSERT INTO "consulta_metrobus_metrobusdata" (id_data, date_updated, vehicle_id,
                            vehicle_label, vehicle_current_status, position_latitude,
                            position_longitude, geographic_point, position_speed,
                            position_odometer, trip_schedule_relationship, trip_id,
                            trip_start_date,
                            trip_route_id, id_alcaldia_id)
                        VALUES ({record["_id"]}, '{record["date_updated"]}', {record["vehicle_id"]},
                            {record["vehicle_label"]}, {record["vehicle_current_status"]}, {record["position_latitude"]},
                            {record["position_longitude"]}, '{record["geographic_point"]}', {record["position_speed"]},
                            {record["position_odometer"]}, {record["trip_schedule_relationship"]}, {record["trip_id"] if record["trip_id"]  else 'null'},
                            {record["trip_start_date"] if record["trip_start_date"]  else 'null'},
                            {record["trip_route_id"] if record["trip_route_id"]  else 'null'}, {alcaldia_id});
                        """)
            
        conn.commit()
        cur.close()
        conn.close()

    def get_alcaldia_by_name(self, name):
        query = "SELECT id FROM consulta_metrobus_alcaldia al WHERE al.name  = %s"
        return self.__execute_query__(query, (name,))

    def get_id_alcaldia(self, coordinates):
        #coordinates = (19.3174991607666,-99.18779754638672)
        results = rg.search(coordinates,mode=1)
        alcaldia_name = None
        print(results)
        for result in results:
            alcaldia_name = result["name"]

        print(alcaldia_name)

        q_alcaldia = self.get_alcaldia_by_name(alcaldia_name)
        
        if not q_alcaldia:
            print('esta vacia')
            conn = self.connection()        
            cur = conn.cursor()

            cur.execute(f"""
                        INSERT INTO "consulta_metrobus_alcaldia" (name)
                        VALUES ('{alcaldia_name}');
                        """)
            conn.commit()
            cur.close()
            conn.close()

            q_alcaldia = self.get_alcaldia_by_name(alcaldia_name)
        
        print(q_alcaldia[0][0])

        return q_alcaldia[0][0]

