import json
import requests
import base as bs

#Instacia de la clase base donde tenemos los metodos de la logica del manejo de datos
bs = bs.Base()

#Proceso que inserta registros de la consulta del metrobus y busca su alcaldia en base a las coordenadas dadas.
bs.insert_metrobus_data()