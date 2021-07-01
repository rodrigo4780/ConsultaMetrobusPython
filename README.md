# ConsultaMetrobus

_Proyecto para consultar API de Ubicacion de Unidades de Metrobus y guardar los datos_
_en una base de datos Postgresql para posteriormente exponer un Servicio GraphQl para consulta_

## Comenzando

_A continuación damos las instrucciones del proyecto._

## Construido Con:

_Herramientas ocupadas para el proyecto_

```
Python 3.8 - Django  (Consulta api metrobus,carga de datos y servicio graphQL).
Base de datos Postgresql
```

## Versionado

_Se ocupo Git para el versionado del proyecto._

## Instrucciones

### Diagrama del dise�o de la soluci�n.

_Dentro del proyecto en raiz se encuentra el archivo "Diagrama Proyecto Metrobus.jpg" donde se encuantra el diagrama de la solución._

### Descarga del proyecto 

_Se proporciona la liga para la descarga del proyecto_

```
git clone https://github.com/rodrigo4780/ConsultaMetrobus.git
```
### Montar Base de datos Postgresql

_Se corren los siguientes comandos para montar la base de datos._
_El archivo Dockerfilebase del proyecto trae la configuracion para correr el script de la Base de datos_

```
docker build -t postgresmetrobus -f Dockerfilebase .
docker run --name base -d -p 5432:5432 postgresmetrobus
```

_Se necesita correr el siguiente comando para ver la ip que se asigno al docker_
_Esto es iportante ya que si nos da una ip distinta a la 172.17.0.2 se tiene que sustituir esta ip_
_por el obtenido en la inspecci�n en los comandos siguientes donde aparezca el host._

```
docker inspect base
```

### Montar proceso de consulta

_Este proceso monta el docker que consulta el API de Ubicacion de unidades del metros_
_e inserta los registros en la base de datos, el proceso despues de iniciado corre cada hora_
_Correr los siguientes comandos:_

```
docker build -t consultametrobus -f Dockerfile2 .
docker run -d -e host=172.17.0.2 --name consulta consultametrobus
```

### Montar Servicio API rest

_Se implementa el API que permite consultar la informaci�n almacenada_
_Correr los comandos:_

```
docker build -t serviciometrobus .
docker run -d -p 80:80 -e host=172.17.0.2 --name servicio serviciometrobus
```

_Una ves montado el API podemos hacer la llamada de la siguiente manera:_

_Obtener una lista de las unidades disponibles._
```
http://localhost/api/unidades/get
```

_Obtener el historial de las ubicaciones/fechas de una unidad dado su id._
```
http://localhost/api/unidades/get/497
```

_Obtener una lista de alcaldias disponibles._
```
http://localhost/api/alcaldias/get
```

_Obtener una lista de unidades que hayan estado dentro de una alcaldia._
```
http://localhost/api/alcaldias/get/17
```
