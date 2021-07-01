from consulta_metrobus.models import *

#funcion para dar de alta una alcaldia
def create_alcaldia():
    alcaldias = []

    alcaldia = Alcaldia.objects.create(name='Magdalena Contreras')
    alcaldias.append(alcaldia)

    return alcaldias

#funcion para dar de alta un registro de metrobusData
def create_metrobusdata(id_alcaldia):
    metrobusdata = []
    alcaldia = Alcaldia.objects.get(pk=id_alcaldia)
    metro = MetrobusData.objects.create(vehicle_id=1, id_alcaldia = alcaldia)
    metrobusdata.append(metro)

    return metrobusdata