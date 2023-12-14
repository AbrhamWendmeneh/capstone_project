import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
passwordval=os.getenv('PASSWORD')

# Establish a connection
conn = psycopg2.connect(host="localhost", dbname="rideHealing", user="postgres", password=passwordval, port=5432)

# Create a cursor
curs = conn.cursor()

try:
    # Create users table
    def create_users_table():
        
        curs.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                fullName TEXT NOT NULL,
                phone TEXT NOT NULL,
                role TEXT NOT NULL,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rating INTEGER
            )
        """)
        conn.commit()

    # Register a user
    def register_user(user, role):
        
        create_users_table()
        curs.execute(
            """
            INSERT INTO users (username, fullName, phone, role)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            """, (user.username, user.fullName, user.phone, role)
        )
        
    def update_user_profile(username, fullName=None, phone=None, role=None):
        
        curs.execute("UPDATE users SET fullName=%s, phone=%s, role=%s WHERE username=%s",(username, fullName, phone, role))

    # Authenticate a user
    def authenticate_user(phone):
        
        curs.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        return curs.fetchone() is not None
    
    def get_user_data(phone):
        
        curs.execute("SELECT * FROM users WHERE phone =%s",(phone))
        return curs.fetchone()
    
    
    
    def get_users_role():
        
        curs.execute("SELECT * FROM users WHERE role=%s",("driver"))
        driver_ids= [val[0] for val in curs.fetchall()]
        return driver_ids
        
            # msg.bot.send()

    # Create rides table
    def create_rides_table():
        
        curs.execute("""
            CREATE TABLE IF NOT EXISTS rides (
                ride_id SERIAL PRIMARY KEY,
                accepted_driver_id INTEGER REFERENCES users(user_id) NOT NULL,
                start_location TEXT NOT NULL,
                destination TEXT NOT NULL,
                estimated_arrival_time TIMESTAMP,
                fare_estimate NUMERIC,
                status TEXT DEFAULT 'pending'
            )
        """)
        
        conn.commit()
        
    def insert_rides(user_id,start_location,destination,estimated_arrival_time,fare_estimate,status):
        
        curs.execute("""
                INSERT INTO rides (user_id, start_location, destination, estimated_arrival_time, fare_estimate, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, 
                (user_id, start_location, destination, estimated_arrival_time, fare_estimate, status)
                )
        
    def is_ride_pending(ride_id):
        
        curs.execute(
            """
            SELECT status FROM rides WHERE ride_id=%s
            
            """,
            (ride_id)
        )
        
        status=curs.fetchone()
        return status==("pending")
        
    def get_ride_id(ride_id):
        
        curs.execute("SELECT * FROM rides WHERE ride_id=%s", (ride_id,))
        return curs.fetchone()
    
    def update_ride_status(ride_id, driver_id, new_status):
        
        curs.execute("UPDATE rides SET status = %s WHERE ride_id = %s", (new_status, ride_id))
        
    def get_accepted_driver_id(ride_id):
        
        curs.execute(
            "SELECT accepted_driver_id FROM rides WHERE ride_id=%s AND AND status = 'accepted' ",(ride_id)
        )
        result=curs.fetchone()
        
        if result:
            
            return result[0]
        
        return None
    
    def get_driver_details(driver_id):
        
        curs.execute(
            "SELECT fullName, phone FROM users WHERE user_id = %s",(driver_id)
        )
        
        return curs.fetchone()

    def update_accepted_driver_id(ride_id, driver_id):
        
        curs.execute(
            "UPDATE rides  SET driver_id = %s, status = 'accepted' WHERE ride_id = %s AND status = 'pending'",(driver_id, ride_id)
        )
        

    
    # This is for the section of inserting values to the table
    # def register_user_ride(user):
    #     create_rides_table
    #     curs.execute(
    #         """
    #         INSERT INTO users (user_id, start_location, destination, status)
    #         VALUES (%s, %s, %s, %s)
    #         ON CONFLICT (username) DO NOTHING
    #         """, (user.user_id, user.start_location, user.destination,)
    #     )
    # Create driver alerts table
    
    def create_driver_alerts():
        
        curs.execute("""
            CREATE TABLE IF NOT EXISTS driver_alerts (
                alert_id SERIAL PRIMARY KEY,
                ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                driver_id INTEGER REFERENCES users(user_id) NOT NULL,
                alert_type VARCHAR(20) NOT NULL
            )
        """)
        
        conn.commit()

    # create rating_reviews table
    def create_rating_reviews():
        
        curs.execute(
                    """
                        CREATE TABLE IF NOT EXISTS rating_reviews (
                            review_id SERIAL PRIMARY KEY,
                            ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                            passenger_id INTEGER REFERENCES users(user_id) NOT NULL,
                            driver_id INTEGER REFERENCES users(user_id) NOT NULL,
                            passenger_rating INTEGER CHECK (passenger_rating >= 1 AND passenger_rating <= 5),
                            driver_rating INTEGER CHECK (driver_rating >= 1 AND driver_rating <= 5),
                            passenger_review TEXT,
                            driver_review TEXT
                        )
                    """
                    )
        
        conn.commit()
        
    # to do 
    # def save_rating(user_id,driver_id,rating):
        
    #     curs.execute(
    #         "INSERT INTO rating_reviews SET"
    #     )

    # Create ride_history table
    def create_ride_history():
        
        curs.execute("""
            CREATE TABLE IF NOT EXISTS ride_history (
                history_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(user_id) NOT NULL,
                start_location REFERENCES rides(start_location),
                destination REFERENCES rides(destination)
                ride_id INTEGER REFERENCES rides(ride_id) NOT NULL,
                completion_time TIMESTAMP
            )
        """)
        
        conn.commit()
        
    def get_history_details(user_id):
        
        curs.execute(
            "SELECT start_location, destination FROM ride_history WHERE user_id= %s",(user_id)
        )
        
        return curs.fetchall()


except Exception as err:
    
    print(f"Error: {err}")
    
finally:
    
    curs.close()
    conn.close()


