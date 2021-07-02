import os
import psycopg2
import requests
import reverse_geocoder as rg
from django.conf import settings

#url para consulta del api del metrobus, donde obtenemos los registros.
URLAPIMETROBUS = 'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e&limit=100'


#Clase Base para la logica de consulta de api e insercion de datos.
class Base():
    def __init__(self):
        #set de los valores para la conexion a la Base de datos.   
        self.DATABASE_NAME = os.getenv('DATABASE_NAME', 'postgres')
        self.DATABASE_USERNAME =  os.getenv('DATABASE_USERNAME', 'postgres')
        self.DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'localdb')
        self.DATABASE_HOST = os.getenv('HOSTBASE', 'localhost')
        self.DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)

    #Función para la creación de la conexión.
    def connection(self):
            conn = psycopg2.connect(database=self.DATABASE_NAME, 
                                    user=self.DATABASE_USERNAME, 
                                    password=self.DATABASE_PASSWORD, 
                                    host=self.DATABASE_HOST, 
                                    port=self.DATABASE_PORT)
            return conn

    #Función para la ejecución de queries.
    def __execute_query__(self, query, values = None):
        
        conn = self.connection()        
        cur = conn.cursor()

        cur.execute(query, values)
        items = cur.fetchall()        
        cur.close()
        conn.close()
        
        return items 

    #Función para la insercion de registros en la BD
    def insert_metrobus_data(self):
        #Creamos la conexión de la BD
        conn = self.connection()        
        cur = conn.cursor()
        
        #Llamada a la api del metrobus
        r = requests.get(URLAPIMETROBUS)
        #Obtenemos el Json de la respuesta.
        metrobusJson = r.json()
        #Dentro del Json obtenemos el nodo de result
        result = metrobusJson['result']
        #Y dentro de result obtenemos el nodo de records que son los registros que insertaremos en la BD
        records = result['records']
        
        #Barremos la lista de los registros.
        for record in records:
            #Obtenemos las coordenadas del registro
            coordinates = (record["position_latitude"], record["position_longitude"])

            #Se manda llamar la funcion para obtener la alcaldia en base a las coordenadas
            alcaldia_id = self.get_id_alcaldia(coordinates)

            #Insertamos el registro ya con nuestra alcaldia.
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

        #Damos commmit a la transaccion, cerramos el cursor y la conexión    
        conn.commit()
        cur.close()
        conn.close()

    #Funcion para validar si existe nuestra alcaldia en la BD.
    def get_alcaldia_by_name(self, name):
        query = "SELECT id FROM consulta_metrobus_alcaldia al WHERE al.name  = %s"
        return self.__execute_query__(query, (name,))

    #Funcion para obtener el id de la alcaldia, si no existe, se da de alta.
    def get_id_alcaldia(self, coordinates):
        #Se llama el reverse_geocoder con las coordenadas 
        #(add-on de django para obtener direcciones en base a lon y lat)
        results = rg.search(coordinates,mode=1)
        alcaldia_name = None

        #obtenemos el nombre de la alcaldia en base a la respuesta de reverse_geocoder
        for result in results:
            alcaldia_name = result["name"]

        #Validamos si existe la alcaldia
        q_alcaldia = self.get_alcaldia_by_name(alcaldia_name)
        
        #Si no existe la damos de alta
        if not q_alcaldia:
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

        # regresamos el id de la alcaldia que obtuvimos por las coordenadas (latitud y longitud)
        return q_alcaldia[0][0]

