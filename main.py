from db.funcs import get_player_users_ids, insert_trip, insert_hotel_trip, insert_expense, insert_expense_trip, insert_flight_trip, insert_flight
from utils.vars import USERS
from sap.funcs import SAP


sap = SAP()

for name, external_id in USERS.items():
    player_user_id = get_player_users_ids(external_id, 147)
    full_trip = sap.get_full_trip(name, external_id, player_user_id)
    for trip in full_trip['trips']:
        trip_id = insert_trip(trip)
        hoteis = trip['hoteis']
        expenses_trip = trip['custos_viagem']

        for hotel in hoteis:
            hotels_trip = hotel['hotels_trip']
            hotels_trip['trip_id'] = trip_id
            hotel_trip_id = insert_hotel_trip(hotels_trip)
            print('Hotel Trip ID:', hotel_trip_id)


        # for expense_trip in expenses_trip:
        #     expense_trip['trip_id'] = trip_id
        #     expense_trip_id = insert_expense_trip(expense_trip)
        #     print('Expense Trip ID:', expense_trip_id)
        #     expenses = expense_trip['expenses']
        #     for expense in expenses:
        #         expense['expenses_trip_id'] = expense_trip_id

        #         expense_id = insert_expense(expense)

        #         print('Expense ID:', expense_id)

        for flight_trip in trip['voos']:
            flight_trip['trip_id'] = trip_id
            flights_trip_id = insert_flight_trip(flight_trip)

            print('Flight Trip ID:', flights_trip_id)

            flight = flight_trip['flight']
            flight['flights_trip_id'] = flights_trip_id
            flight_id = insert_flight(flight)
            print('Flight ID:', flight_id)
