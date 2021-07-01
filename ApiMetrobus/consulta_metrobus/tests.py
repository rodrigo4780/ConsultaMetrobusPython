import graphene
from consulta_metrobus.schema import Query
from consulta_metrobus.utilities import *
from django.test import TestCase
from graphene.test import Client

#Pruebas unitarias para la api de metrobus graphql
class MetrobusDataTestCase(TestCase):

    #Setup para crear los registros con los que se harán las pruebas unitarias
    def setUp(self):
        self.alcaldias = create_alcaldia()
        self.metrobusdata = create_metrobusdata(self.alcaldias[0].id)
        super().setUp()

        #Querys de las 4 consultas solicitadas en la prueba
        self.queryUnidDisp = """
            query {
              unidadesDisponibles {
                vehicleId
              }
            }
        """

        self.queryUbiUni = """
            query{
                ubicacionesUnidad(unidadId:1){
                    idAlcaldia{
                    name
                    }
                }
            }
        """

        self.queryAlcaldias = """
            query{
                allAlcaldias{
                    name
                }
            }
        """

        self.queryUnidAlcad = """
            query{{
                unidadesAlcaldia(alcaldiaId:{id_alcaldia}){{
                    vehicleId
                    idAlcaldia{{
                        name
                    }}
                }}
            }} 
        """.format(id_alcaldia=self.alcaldias[0].id)

    #Prueba para unidades disponibles
    def test_unidades_disponibles(self):
        schema = graphene.Schema(query=Query)
        result = schema.execute(self.queryUnidDisp)
        expected = {"unidadesDisponibles": [{"vehicleId": 1}]}
        self.assertIsNone(result.errors)
        self.assertDictEqual(expected, result.data)
    
    #Prueba para Historial de ubicaciones
    def test_HistorialUbicaciones(self):
        schema = graphene.Schema(query=Query)
        result = schema.execute(self.queryUbiUni)
        expected = {"ubicacionesUnidad": [{"idAlcaldia": {"name": "Magdalena Contreras"}}]}
        self.assertIsNone(result.errors)
        self.assertDictEqual(expected, result.data)

    #Prueba para alcaldias existentes
    def test_alcaldias(self):
        schema = graphene.Schema(query=Query)
        result = schema.execute(self.queryAlcaldias)
        expected = {"allAlcaldias": [{"name": "Magdalena Contreras"}]}
        self.assertIsNone(result.errors)
        self.assertDictEqual(expected, result.data)

    #Prueba para unidades por alcaldia
    def test_unidades_alcaldia(self):
        schema = graphene.Schema(query=Query)
        result = schema.execute(self.queryUnidAlcad)
        expected = {"unidadesAlcaldia": [{"vehicleId": 1, "idAlcaldia": {"name": "Magdalena Contreras"}}]}
        self.assertIsNone(result.errors)
        self.assertDictEqual(expected, result.data)