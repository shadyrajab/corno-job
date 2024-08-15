from .conn import CONNECTION

def get_player_users_ids(external_id, player_company_id):
    cursor = CONNECTION.cursor()
    cursor.execute("SELECT id FROM player_users where external_id = %s and player_company_id = %s", (external_id, player_company_id))
    return cursor.fetchone()[0]


def insert_flight(flight):
    print(flight)
    # cursor = None
    # try:
    #     cursor = CONNECTION.cursor()
    #     cursor.execute("""
    #         INSERT INTO flights (id, departure_airport_address_id, arrived_airport_address_id, departure_airport_name, departure_airport_code)
    #         VALUES (default, %s, %s, %s, %s)
    #         RETURNING id
    #         """,
    #     (
    #         flight['departure_airport_address_id'],
    #         flight['arrived_airport_address_id'],
    #         flight['departure_airport_name'],
    #         flight['departure_airport_code'],

    pass

def insert_flight_trip(flight_trip):
    cursor = None
    try:
        cursor = CONNECTION.cursor()
        cursor.execute("""
            INSERT INTO flight_trips (id, direction, departure_at, arrived_at, trip_id)
            VALUES (default, %s, %s, %s, %s, %s)
            RETURNING id
        """,
        (
            flight_trip['direction'],
            flight_trip['departure_at'],
            flight_trip['arrived_at'],
            flight_trip['trip_id'],
        ))

        flight_trip_id = cursor.fetchone()[0]
        CONNECTION.commit()
        return flight_trip_id   

    except Exception as e:
        if CONNECTION:
            CONNECTION.rollback()
    finally:
        if cursor:
            cursor.close()

def insert_expense(expense):
    cursor = None
    try:
        cursor = CONNECTION.cursor()
        cursor.execute("""
            INSERT INTO expenses (id, expenses_trip_id, currency_code, code, description)
            VALUES (default, %s, %s, %s)
            RETURNING id
        """,
        (
            expense['expenses_trip_id'],
            int(float(expense['total'])),
            expense['currency_code'],
            expense['code'], 
            expense['description'], 
        ))

        expense_id = cursor.fetchone()[0]
        CONNECTION.commit()
        return expense_id
    except Exception as e:
        if CONNECTION:
            CONNECTION.rollback()
    finally:
        if cursor:
            cursor.close()


def insert_expense_trip(expense_trip):
    cursor = None
    try:
        cursor = CONNECTION.cursor()
        cursor.execute("""
            INSERT INTO expenses_trip (id, total, refund_at, currency_code, trip_id)
            VALUES (default, %s, %s, %s, %s)
            RETURNING id
        """,
        (
            int(float(expense_trip['total'])),
            expense_trip['refund_at'], 
            expense_trip['currency_code'], 
            expense_trip['trip_id']
        ))

        expense_id = cursor.fetchone()[0]
        CONNECTION.commit()
        return expense_id
    except Exception as e:
        if CONNECTION:
            CONNECTION.rollback()
        print(f"Erro ao inserir expense: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

def insert_hotel_trip(hotel_trip):
    print(hotel_trip)
    cursor = None
    try:
        cursor = CONNECTION.cursor()
        cursor.execute("""
            INSERT INTO hotels_trip (id, checkin_at, checkout_at, amount, currency_code, trip_id)
            VALUES (default, %s, %s, %s, %s, %s)
            RETURNING id
        """,
        (
            hotel_trip['checkin_at'], 
            hotel_trip['checkout_at'], 
            int(float(hotel_trip['amount'])),
            hotel_trip['currency_code'], 
            hotel_trip['trip_id']
        ))

        hotel_id = cursor.fetchone()[0]
        CONNECTION.commit()
        return hotel_id
    except Exception as e:
        if CONNECTION:
            CONNECTION.rollback()
        print(f"Erro ao inserir hotel: {e}")
        return None

    finally:
        if cursor:
            cursor.close()


def insert_trip(trip):
    cursor = None
    try:
        cursor = CONNECTION.cursor()
        cursor.execute("""
            INSERT INTO trip (id, start_at, end_at, status, reason, amount, currency_code, player_user_id, external_id) 
            VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id
        """, 
        (
            trip['start_at'], 
            trip['end_at'], 
            trip['status'], 
            trip['reason'], 
            trip['amount'], 
            trip['currency_code'], 
            trip['player_user_id'],
            trip["external_id"]
        ))
        
        trip_id = cursor.fetchone()[0]
        
        CONNECTION.commit()
        
        return trip_id

    except Exception as e:
        if CONNECTION:
            CONNECTION.rollback()
        print(f"Erro ao inserir trip: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

def get_address(address):
    cursor = CONNECTION.cursor()
    cursor.execute("SELECT id FROM addresses where address ILIKE(%s)", (address,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    return ""