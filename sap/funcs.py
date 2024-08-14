import requests 
from utils.vars import BODY, BASE_URL
import json

class SAP:
    def __init__(self):
        access_token = self.login_sap()
        self.headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    def login_sap(self):
        response = requests.post(f"{BASE_URL}/OAuthService/GenerateToken", data=BODY)
        return response.json()['access_token']

    def get_url(self, trip, name):
       return BASE_URL + "/YSTV_APV_ROT_VIAG_SRV/Viagens" + trip[name]['__deferred']['uri'].split("/Viagens")[1]
    
    def get_full_trip(self, name, external_id, player_user_id):
        full_trips = {
            "name": name,
            "external_id": external_id,
            "player_user_id": player_user_id,
            "trips": [],
            "hoteis": [],
            "adiantamentos": [],
            "custos_viagem": [],
            "voos": [],
            "excecoes": [],
            "outros_destinos": [],
            "anexos": []
        }

        trip_url = f"{BASE_URL}/YSTV_APV_ROT_VIAG_SRV/Viagens?search=TRIPEEdataini:20240812,datafim:20240814,pernr:{external_id}"
        response = requests.get(trip_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for trip in results:
                del trip['__metadata']

                hoteis = self.get_hoteis(self.get_url(trip, 'Hoteis'))
                adiantamentos = self.get_adiantamentos(self.get_url(trip, 'Adiantamentos'))
                custos_viagem = self.get_custos_viagem(self.get_url(trip, 'CustosViagem'))
                voos = self.get_voos(self.get_url(trip, 'Voos'))
                excecoes = self.get_excecoes(self.get_url(trip, 'Excecoes'))
                outros_destinos = self.get_outros_destinos(self.get_url(trip, 'OutrosDestinos'))
                anexos = self.get_anexos(self.get_url(trip, 'Anexos'))

                full_trips['adiantamentos'].append(adiantamentos)
                full_trips['hoteis'].append(hoteis)
                full_trips['custos_viagem'].append(custos_viagem)
                full_trips['voos'].append(voos)
                full_trips['excecoes'].append(excecoes)
                full_trips['outros_destinos'].append(outros_destinos)
                full_trips['anexos'].append(anexos)

                full_trips['trips'].append(trip)

        with open(f"json/{name}.json", "w") as f:
            json.dump(full_trips, f)

    def get_hoteis(self, hoteis_url):
        response = requests.get(hoteis_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for hotel in results:
                del hotel['__metadata']
        
        return results

    def get_adiantamentos(self, adiantamentos_url):
        response = requests.get(adiantamentos_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for adiantamento in results:
                del adiantamento['__metadata']
        
        return results

    def get_custos_viagem(self, custos_viagem_url):
        response = requests.get(custos_viagem_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for custo in results:
                del custo['__metadata']
        
        return results

    def get_voos(self, voos_url):
        full_flights = []
        response = requests.get(voos_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for voos in results:
                del voos['__metadata']

        return results

        # if results:
        #     for voos in results:
        #         trip_eta = voos['OrigemHora']
        #         departure_airport_name = voos['OrigemNomeAeroporto']
        #         arrived_airport_name = voos['DestinoNomeAeroporto']
        #         # departure_airport_address_id = 

        #         departure_airport_code = voos['OrigemCidadeAeroporto']
        #         arrived_airport_name = voos['DestinoCidadeAeroporto']
        #         # arrived_airport_address_id =

        #         departure_at = voos['OrigemData']
        #         arrived_at = voos['DestinoData']

        #         # external_id

        #         airline_code = voos['EmpresaAerea']
        #         airline_display_name = voos['EmpresaAereaOferente']
        #         status = voos['Situacao']
                
        #         flight_number = voos['NumVoo']
        #         # booking_number = flight['NumReserva']

        #         # airline_id = flight['Identificador']

        #         full_flights.append[{
        #             "trip_eta": trip_eta,
        #             "departure_airport_name": departure_airport_name,
        #             "arrived_airport_name": arrived_airport_name,
        #             # "departure_airport_code": departure_airport_code,
        #             # "arrived_airport_code": arrived_airport_code,
        #             "departure_at": departure_at,
        #             "arrived_at": arrived_at,
        #             "airline_code": airline_code,
        #             "airline_display_name": airline_display_name,
        #             "status": status,
        #             "flight_number": flight_number
        #         }]

    def get_excecoes(self, excecoes_url):
        response = requests.get(excecoes_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for excecao in results:
                del excecao['__metadata']
        
        return results

    def get_outros_destinos(self, outros_destinos_url):
        response = requests.get(outros_destinos_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for outro_destino in results:
                del outro_destino['__metadata']
        
        return results

    def get_anexos(self, anexos_url):
        response = requests.get(anexos_url, headers=self.headers).json()
        results = response['d']['results']

        if results:
            for anexo in results:
                del anexo['__metadata']
        
        return results