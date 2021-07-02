# ConsultaMetrobus

_Proyecto para consultar API de Ubicacion de Unidades de Metrobus y guardar los datos_
_en una base de datos Postgresql para posteriormente exponer un Servicio GraphQl para consulta_

## Resumen

_Para completar la prueba tecnica se realizo lo siguiente:_

_Diagrama con el diseño de la solución_

_Script python  que consulta API Metrobus y Obtiene alcaldia en base a coordenadas de_
_       cada registro, el cual inserta en la base de datos._
_Se crea App consulta_metrobus en el proyecto para el _
_       API Graphql que entrega las consultas solicitadas._
_Se crea el archivo Dockerfile para empaquetar el servicio._
_Se crea dentro del App consulta_metrobus las respectivas pruebas unitarias.(tests.py)_


## Construido Con:

_Herramientas ocupadas para el proyecto_

```
Python 3.8 - Django  (Consulta api metrobus,carga de datos y servicio graphQL).
Base de datos Postgresql
```

## Versionado

_Se ocupo Git para el versionado del proyecto._

## Instrucciones

### Diagrama del diseño de la solución.

_Dentro del proyecto en raiz se encuentra el archivo "Diagrama Metrobus.JPG" donde se encuantra el diagrama de la solución._

### Descarga del proyecto 

_Se proporciona la liga para la descarga del proyecto_

```
git clone https://github.com/rodrigo4780/ConsultaMetrobusPython.git
```
### Montar Base de datos Postgresql

_Se corren el siguiente comando para montar la base de datos._

```
docker run -d --rm --name metrobus -e POSTGRES_PASSWORD=localdb -p 5432:5432 postgres
```

_Se necesita correr el siguiente comando para ver la ip que se asigno al docker_
_Esto es iportante ya que si nos da una ip distinta a la 172.17.0.2 se tiene que sustituir esta ip_
_por el obtenido en la inspección en el archivo dockerfile en la variable de ambiente HOSTBASE._

```
docker inspect base
```

### Proceso de consulta y llenado a la base de datos.

_En los pasos siguientes pasos se consulta el API de Ubicacion de unidades del metros_
_e inserta los registros en la base de datos_
_Correr los siguientes comandos:_

_Descargar el codigo:_

```
git clone https://github.com/rodrigo4780/ConsultaMetrobusPython.git
```

_Crear ambiente de python:_

```
python -m venv env
```
_Una vez creado al ambiente corremos el archivo "Activate"_
_A continuación se instalan las librerias necesarias_

```
pip install -r requirements.txt
```


_Nos cambiamos a la ruta del proyecto dentro de la carpeta ApiMetroubus_ 
_al nivel del archivo manage.py y corremos los siguientes comandos:_

```
python manage.py migrate
python consultaunidades.py
```
Estos comandos crean la estructura de la BD
y el script de python que consulta el API de metrobus y guarda los registros


### Pruebas unitarias.

_Para correr las pruebas unitarias se corre el siguiente comando._

```
python manage.py test consulta_metrobus.tests
```


### Montar Servicio Graphql

_Se implementa el API GraphQL que permite consultar la información almacenada_
_Correr los comandos:_

```
docker build -t serviciometrobus .
docker run -d -p 8080:8080 --name servicio serviciometrobus
```

_Una ves montado el Docker podemos hacer la llamada desde la siguiente liga:_

```
http://localhost:8080/graphql/
```

_Dentro corremos los siguientes querys para las consultas solicitadas:_


_Query para obtener las unidades disponibles._
```
query {
  unidadesDisponibles {
    vehicleId
  }
}
```

_Query para obtener el historial de las ubicaciones/fechas de una unidad dado su id._
```
query{
  ubicacionesUnidad(unidadId:24){
    idAlcaldia{
      name
    }
    dateUpdated
  }
}
```

_Query para obtener una lista de alcaldias disponibles._
```
query{
  allAlcaldias{
    id
    name
  }
}
```

_Query para obtener una lista de unidades que hayan estado dentro de una alcaldia._
```
query{
  unidadesAlcaldia(alcaldiaId:2){
    vehicleId
    idAlcaldia{
      name
    }
  }
}
```
