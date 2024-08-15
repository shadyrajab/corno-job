import requests 
from utils.vars import BODY, BASE_URL
import json
from db.funcs import get_address
from datetime import datetime, timezone
import re

status_map = {
    '1': 'CRIADA',
    '2': 'APROVADA',
    '3': 'PC_REALIZADA',
    '4': 'PC_APROVADA'
};

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
            "trips": [],
        }

        trip_url = f"{BASE_URL}/YSTV_APV_ROT_VIAG_SRV/Viagens?search=TRIPEEdataini:20240812,datafim:20240814,pernr:{external_id}"
        response = requests.get(trip_url, headers=self.headers)
        content = response.content.decode('utf-8')
        response = json.loads(content)
        results = response['d']['results']

        if results:
            for trip in results:
                del trip['__metadata']

                hoteis = self.get_hoteis(self.get_url(trip, 'Hoteis'), external_id)
                adiantamentos = self.get_adiantamentos(self.get_url(trip, 'Adiantamentos'))
                custos_viagem = self.get_custos_viagem(self.get_url(trip, 'CustosViagem'), adiantamentos)
                voos = self.get_voos(self.get_url(trip, 'Voos'), external_id)

                start_at, end_at = trip['Periodo'].split("Até")
                start_at_dt = datetime.strptime(start_at.strip(), '%d.%m.%Y')
                end_at_dt = datetime.strptime(end_at.strip(), '%d.%m.%Y')

                trip = {
                    "start_at": start_at_dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "end_at": end_at_dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "status": status_map.get(trip["Status"]),
                    "reason": trip["MotivoViagem"],
                    "external_id": external_id,
                    "amount": trip["PrecoTotalPassagem"],
                    "player_user_id": player_user_id,
                    "currency_code": trip["MoedaPrecoTotal"],
                    "hoteis": hoteis,
                    "custos_viagem": custos_viagem,
                    "voos": voos
                }
                
                full_trips['trips'].append(trip)

        with open(f"json/{name}.json", "w") as f:
            json.dump(full_trips, f)

        return full_trips

    def stract_date(self, date_string):
        if not date_string:
            return None
        timestamp = int(re.search(r'\d+', date_string).group())
        timestamp /= 1000
        date_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)

        return date_time.strftime('%Y-%m-%d %H:%M:%S')


    def get_hoteis(self, hoteis_url, external_id):
        hotels = []
        response = requests.get(hoteis_url, headers=self.headers)
        content = response.content.decode('utf-8')
        response = json.loads(content)

        results = response['d']['results']

        if results:
            for hotel in results:
                del hotel['__metadata']

                hotel = {
                    "external_id": external_id,
                    "name": hotel["Nome"],
                    "address_id": get_address(hotel["Endereco"]),
                    "hotels_trip": {
                        "checkin_at": self.stract_date(hotel["DataChegada"]),
                        "checkout_at": self.stract_date(hotel["DataSaida"]),
                        "amount": hotel["PrecoTotal"],
                        "currency_code": hotel["Moeda"],
                        "trip_id": ""
                    }
                }

                hotels.append(hotel)
        
        return hotels

    def get_adiantamentos(self, adiantamentos_url):
        response = requests.get(adiantamentos_url, headers=self.headers)
        content = response.content.decode('utf-8')
        response = json.loads(content)
        results = response['d']['results']

        if results:
            for adiantamento in results:
                del adiantamento['__metadata']
        
        return results

    def get_custos_viagem(self, custos_viagem_url, adiantamentos):
        expenses = []
        response = requests.get(custos_viagem_url, headers=self.headers)
        content = response.content.decode('utf-8')
        response = json.loads(content)
        results = response['d']['results']

        if results:
            for custo in results:
                expenses_trip = {
                    "total": custo["Valor"],
                    "refund_at": None,
                    "currency_code": custo["Moeda"],
                    "trip_id": "",
                    "expenses": [{
                        "expenses_trip_id": "",
                        "total": adiantamento["Valor"],
                        "currency_code": adiantamento["Moeda"],
                        "code": adiantamento["Tipo"],
                        "description": adiantamento["Descricao"],
                    } for adiantamento in adiantamentos]
                }

                expenses.append(expenses_trip)
        
        return expenses

    def get_voos(self, voos_url, external_id):
        flights = []
        response = requests.get(voos_url, headers=self.headers)
        content = response.content.decode('utf-8')
        response = json.loads(content)
        results = response['d']['results']

        if results:
            for voos in results:
                del voos['__metadata']

                flight = {
                    "direction": "",
                    "departure_at": self.stract_date(voos["OrigemData"]),
                    "arrived_at": self.stract_date(voos["DestinoData"]),
                    "trip_id": "",
                    "flight": {
                        "departure_airport_address_id": get_address(voos["OrigemNomeAeroporto"]),
                        "arrived_airport_address_id": get_address(voos["DestinoNomeAeroporto"]),

                        "departure_airport_name": voos["OrigemNomeAeroporto"],
                        "departure_airport_code": voos["OrigemCidadeAeroporto"],
                        "departure_at": self.stract_date(voos["OrigemData"]),

                        "arrived_airport_name": voos["DestinoNomeAeroporto"],
                        "arrived_airport_code": voos["DestinoCidadeAeroporto"],
                        "arrived_at": self.stract_date(voos["DestinoData"]),
                        "trip_eta": "",
                        "external_id": external_id,
                        "status": voos["Situacao"],
                        "airline_code": voos["EmpresaAerea"],
                        "airline_display_name": voos["EmpresaAereaOferente"],
                        "sequence_flight": "",
                        "fligh_trips_id": "",
                        "flight_number": voos["NumVoo"],
                        "booking_number": "",
                        "airline_id": "",
                    }
                }

                flights.append(flight)

        return flights

