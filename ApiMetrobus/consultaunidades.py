import json
import requests
import reverse_geocoder as rg
import base as bs

bs = bs.Base()

#acceso al servicio web del metrobus
r = requests.get('https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e&limit=5')
metrobusJson = r.json()
result = metrobusJson['result']
records = result['records']

bs.insert_metrobus_data(records)