from datetime import datetime
import database as dbl

def create_reservation(user_id, equipment_id, start_time_str, end_time_str):
    """
    Attempts to create a reservation. Validates time logic, checks equipment status, 
    prevents double-booking, and handles the waitlist.
    
    Returns a dictionary: {'status': 'success' | 'waitlist' | 'error', 'message': str}
    """
    # --- Constraint 1: Basic Time Validation ---
    try:
        # If your HTML form uses datetime-local, the format might be '%Y-%m-%dT%H:%M'
        # Adjust the format string below if your HTML input format differs
        start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
        
        if start_time < datetime.now():
            return {'status': 'error', 'message': "You cannot book equipment in the past."}
        if end_time <= start_time:
            return {'status': 'error', 'message': "End time must be after the start time."}
    except ValueError:
        return {'status': 'error', 'message': "Invalid date/time format submitted."}

    # --- Database Operations ---
    db = dbl.get_db_connection()
    # Using DictionaryCursor if supported by your driver, otherwise normal tuples work
    cursor = db.cursor() 

    try:
        # --- Constraint 2: Is the equipment broken? ---
        cursor.execute("SELECT name, status FROM equipment WHERE equipment_id = %s", (equipment_id,))
        equip = cursor.fetchone()

        if not equip:
            return {'status': 'error', 'message': "Equipment not found."}

        # Handle tuple return (if not using DictionaryCursor)
        equip_name = equip[0] if isinstance(equip, tuple) else equip['name']
        equip_status = equip[1] if isinstance(equip, tuple) else equip['status']

        if equip_status == 'repair':
            _add_to_waitlist(cursor, db, user_id, equipment_id)
            return {'status': 'waitlist', 'message': f"🚫 {equip_name} is currently out for repair. You've been added to the waitlist."}

        # --- Constraint 3: Time Overlap Conflict ---
        conflict_query = """
            SELECT reservation_id FROM reservations 
            WHERE equipment_id = %s AND status = 'active'
              AND start_time < %s AND end_time > %s
        """
        # Notice we compare with the string versions for the SQL query
        cursor.execute(conflict_query, (equipment_id, end_time_str, start_time_str))
        conflicts = cursor.fetchall()
        
        if len(conflicts) > 0:
            _add_to_waitlist(cursor, db, user_id, equipment_id)
            return {'status': 'waitlist', 'message': f"⚠️ {equip_name} is already booked during this time. You've been added to the waitlist."}

        # --- Constraint 4: Success, Book it! ---
        insert_res_query = """
            INSERT INTO reservations (user_id, equipment_id, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, 'active')
        """
        cursor.execute(insert_res_query, (user_id, equipment_id, start_time_str, end_time_str))
        db.commit()
        
        return {'status': 'success', 'message': f"✅ Success! Your reservation for {equip_name} is confirmed."}

    except Exception as e:
        db.rollback()
        return {'status': 'error', 'message': f"Database Error: {str(e)}"}
    finally:
        cursor.close()
        db.close()


def _add_to_waitlist(cursor, db, user_id, equipment_id):
    """
    Private helper function to add users to the waitlist.
    Does not open/close its own connection; uses the active transaction.
    """
    waitlist_query = "INSERT INTO waitlist (user_id, equipment_id) VALUES (%s, %s)"
    cursor.execute(waitlist_query, (user_id, equipment_id))
    db.commit()