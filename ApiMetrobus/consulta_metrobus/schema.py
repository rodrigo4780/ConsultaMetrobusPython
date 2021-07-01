import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from .models import Alcaldia, MetrobusData

#Creacion de tipo para alcaldia
class AlcaldiaType(DjangoObjectType): 
    class Meta:
        model = Alcaldia
        fields = "__all__"


#Creacion de tipo para MetrobusData
class MetrobusDataType(DjangoObjectType):
    class Meta:
        model = MetrobusData
        fields = "__all__"


#Query para la consulta de graphql
class Query(graphene.ObjectType):
    #Se definen las listas para las consultas del api
    unidades_disponibles = graphene.List(MetrobusDataType)
    ubicaciones_unidad = graphene.List(MetrobusDataType, unidad_id=graphene.Int())
    all_alcaldias = graphene.List(AlcaldiaType)
    unidades_alcaldia = graphene.List(MetrobusDataType, alcaldia_id=graphene.Int())


    #Se crean los resolves para las consultas
    def resolve_unidades_disponibles(self, info, **kwargs):
        return MetrobusData.objects.all().distinct('vehicle_id').order_by('vehicle_id')

    def resolve_ubicaciones_unidad(self, info, unidad_id):
        return MetrobusData.objects.filter(vehicle_id=unidad_id)

    def resolve_all_alcaldias(self, info, **kwargs):
        return Alcaldia.objects.all()

    def resolve_unidades_alcaldia(self, info, alcaldia_id):
        return MetrobusData.objects.filter(id_alcaldia__id=alcaldia_id)


schema = graphene.Schema(query=Query)