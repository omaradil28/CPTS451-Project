from datetime import datetime, timedelta
import database as dbl

def get_bookings(user_id):

    db = dbl.get_db_connection()
    cursor = db.cursor()

    user_bookings = []
    
    query = """SELECT *
                FROM reservations
                WHERE user_id = %s;"""
    
    cursor.execute(query, user_id)

    for row in cursor.fetchall():
        user_bookings.append(
            {
                "reservation_id": row[0],
                "user_id": row[1],
                "equipment_id": row[2],
                "start_time": row[3],
                "end_time": row[4],
                "status": row[5],
            }
        )
    
    return user_bookings

def cancel_booking(reservation_id):

    db = dbl.get_db_connection()
    cursor = db.cursor()

    query = """SELECT *
                FROM reservations 
                WHERE reservation_id = %s;"""