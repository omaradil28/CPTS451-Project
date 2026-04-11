from datetime import datetime, timedelta
import database as dbl

def create_reservation(user_id, equipment_id, start_time_str, end_time_str):
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
        
        duration = end_time - start_time
        if duration.total_seconds() > 14400:
            return {'status': 'error', 'message': "Bookings cannot exceed 4 hours."}

        if start_time < datetime.now():
            return {'status': 'error', 'message': "Cannot book in the past."}
            
        if end_time <= start_time:
            return {'status': 'error', 'message': "End time must be after start time."}

        max_future = datetime.now() + timedelta(days=14)
        if start_time > max_future:
            return {'status': 'error', 'message': "Maximum 14 days in advance."}
            
    except ValueError:
        return {'status': 'error', 'message': "Invalid format."}

    db = dbl.get_db_connection()
    cursor = db.cursor() 

    try:
        conflict_query = """
            SELECT * FROM reservations 
            WHERE equipment_id = %s AND status = 'active'
              AND start_time < %s AND end_time > %s
        """
        cursor.execute(conflict_query, (equipment_id, end_time_str, start_time_str))
        if cursor.fetchone():
            return {'status': 'error', 'message': "Time slot already taken."}

        cursor.execute("""
            INSERT INTO reservations (user_id, equipment_id, start_time, end_time, status)
            VALUES (%s, %s, %s, %s, 'active')
        """, (user_id, equipment_id, start_time_str, end_time_str))
        
        db.commit()
        return {'status': 'success', 'message': "Confirmed!"}

    except Exception as e:
        db.rollback()
        return {'status': 'error', 'message': str(e)}
    finally:
        cursor.close()
        db.close()