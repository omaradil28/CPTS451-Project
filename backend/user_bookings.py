from datetime import datetime, timedelta
import database as dbl

def get_bookings(user_id):

    db = dbl.get_db_connection()
    cursor = db.cursor()

    user_bookings = []
    
    query = """SELECT *
                FROM reservations
                WHERE user_id = %s;"""
    
    cursor.execute(query, (user_id,))

    for row in cursor.fetchall():
        bookingDict = {
                "reservation_id": row["reservation_id"],
                "user_id": row["user_id"],
                "equipment_id": row["equipment_id"],
                "start_time": row["start_time"],
                "end_time": row["end_time"],
                "status": row["status"],
            }
        
        name_cursor = db.cursor()
        name_query = """SELECT *
                        FROM equipment
                        WHERE equipment_id = %s"""
        name_cursor.execute(name_query, (bookingDict["equipment_id"],))
        bookingDict["equipment_name"] = name_cursor.fetchone()["name"]

        user_bookings.append(bookingDict)
    
    return user_bookings

def cancel_booking(reservation_id):

    db = dbl.get_db_connection()
    cursor = db.cursor()

    query = """UPDATE reservations
                SET status = 'cancelled'
                WHERE reservation_id = %s;"""
    
    cursor.execute(query, (reservation_id,))
    db.commit()