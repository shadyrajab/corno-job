from .conn import CONNECTION

def get_player_users_ids(external_id, player_company_id):
    cursor = CONNECTION.cursor()
    cursor.execute("SELECT id FROM player_users where external_id = %s and player_company_id = %s", (external_id, player_company_id))
    return cursor.fetchone()[0]


def insert_trip(trip, external_id, player_user_id):
    print(trip)