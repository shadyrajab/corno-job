from db.funcs import get_player_users_ids, insert_trip
from utils.vars import USERS
from sap.funcs import SAP


sap = SAP()

for name, external_id in USERS.items():
    player_user_id = get_player_users_ids(external_id, 147)
    full_trip = sap.get_full_trip(name, external_id, player_user_id)

    trip = insert_trip(full_trip['trips'], external_id, player_user_id)

# import requests
# from dotenv import config
# import psycopg2
# import os 

# from utils.vars import BASE_URL, USERS
# from utils.funcs import get_url


# config()

# body = {
#   "client_id": os.getenv("client_id"),
#   "client_secret": os.getenv("client_secret"),
#   "grant_type": os.getenv("grant_type"),
# }

# access_token = requests.post(f"{BASE_URL}/OAuthService/GenerateToken", data=body).json()['access_token']
# headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

# connection = psycopg2.connect(
#   dbname=os.getenv("dbname"),
#   user=os.getenv("user"),
#   password=os.getenv("password"),
#   host=os.getenv("host"),
# )

# def insert_trip(trip, external_id):
#     start_at, end_at = trip['Periodo'].split("Até")
#     status = trip['Status'] # Tem que formatar pois o status vem em valor numérico
#     reason = trip['MotivoViagem']
#     amount = trip['PrecoTotalPassagem']
#     currency_code = trip['MoedaPrecoTotal']
#     # player_user_id = trip['Matricula'] # Tem que saber onde pega o maldito player_user

    




#     print(trip)

# def insert_fligh_trip():
#     pass

# def insert_trip_agency():
#     pass

# def insert_flights(url, external_id):
#     flights = requests.get(url, headers=headers).json()
#     results = flights['d']['results']

#     if results:
#         for flight in results:
#             del flight['__metadata']
            
#             trip_eta = flight['OrigemHora']
#             departure_airport_name = flight['OrigemNomeAeroporto']
#             arrived_airport_name = flight['DestinoNomeAeroporto']
#             # departure_airport_address_id = 

#             departure_airport_code = flight['OrigemCidadeAeroporto']
#             arrived_airport_name = flight['DestinoCidadeAeroporto']
#             # arrived_airport_address_id =

#             departure_at = flight['OrigemData']
#             arrived_at = flight['DestinoData']

#             # external_id

#             airline_code = flight['EmpresaAerea']
#             airline_display_name = flight['EmpresaAereaOferente']
#             status = flight['Situacao']
            
#             flight_number = flight['NumVoo']
#             # booking_number = flight['NumReserva']

#             # airline_id = flight['Identificador']
            

# def insert_expenses(url):
#     # Tabela public.expenses
#     expenses = requests.get(url, headers=headers).json()
#     results = expenses['d']['results']

#     if results:
#         for expense in results:
#             del expense['__metadata']

#             total = expense['Valor']
#             moeda = expense['Moeda']

#             # Resta saber onde está as colunas description e code
#             print(expense)

# for key, value in USERS.items():
#     url = f"{BASE_URL}/YSTV_APV_ROT_VIAG_SRV/Viagens?search=TRIPEEdataini:20240812,datafim:20240814,pernr:{value}"
#     # print(url)
#     trip = requests.get(url, headers=headers).json()
#     results = trip['d']['results']
#     if results:

#         for trip in results:
#             del trip['__metadata']
            
#             hoteis = get_url(trip, 'Hoteis')
#             adiantamentos = get_url(trip, 'Adiantamentos')
#             custos_viagem = get_url(trip, 'CustosViagem')
#             voos = get_url(trip, 'Voos')
#             excecoes = get_url(trip, 'Excecoes')
#             outros_destinos = get_url(trip, 'OutrosDestinos')
#             anexos = get_url(trip, 'Anexos')

#             checkin_at, checkout_at = trip['Periodo'].split("Até")

#             # insert_expenses(custos_viagem)
#             insert_flights(voos, value)
#             insert_trip(trip)
